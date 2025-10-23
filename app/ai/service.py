import asyncio
import pandas as pd
from datetime import datetime
from app.core.database import AsyncSessionLocal, TradingSignal, AIModel
from app.ai.lstm_model import lstm_predictor
from app.core.config import settings
import yfinance as yf
import numpy as np
from typing import Dict, List

class AISignalService:
    def __init__(self):
        self.is_running = False
        self.active_models = {}
        
    async def initialize_models(self):
        """Inicializa todos os modelos de IA"""
        try:
            # Carregar modelo LSTM
            await lstm_predictor.load_model()
            self.active_models["lstm"] = lstm_predictor
            print("✅ Modelos de IA inicializados")
        except Exception as e:
            print(f"❌ Erro ao inicializar modelos: {e}")
    
    async def get_market_data(self, symbol: str, period: str = "60d", interval: str = "1h") -> pd.DataFrame:
        """Busca dados de mercado para análise da IA"""
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period, interval=interval)
            
            if data.empty:
                return None
            
            # Adicionar indicadores básicos
            data['SMA_20'] = data['Close'].rolling(window=20).mean()
            data['SMA_50'] = data['Close'].rolling(window=50).mean()
            data['EMA_12'] = data['Close'].ewm(span=12).mean()
            data['EMA_26'] = data['Close'].ewm(span=26).mean()
            
            # RSI
            delta = data['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            data['RSI'] = 100 - (100 / (1 + rs))
            
            # MACD
            data['MACD'] = data['EMA_12'] - data['EMA_26']
            
            # Volume
            data['Volume_SMA'] = data['Volume'].rolling(window=20).mean()
            
            return data.dropna()
            
        except Exception as e:
            print(f"Erro ao buscar dados para {symbol}: {e}")
            return None
    
    async def analyze_with_ai(self, symbol: str) -> Dict:
        """Analisa um símbolo usando IA"""
        try:
            # Buscar dados
            data = await self.get_market_data(symbol)
            if data is None or len(data) < 100:
                return {"error": "Dados insuficientes"}
            
            # Usar LSTM para previsão
            lstm_result = await lstm_predictor.predict(data)
            
            if "error" in lstm_result:
                return lstm_result
            
            # Análise técnica adicional
            current_rsi = data['RSI'].iloc[-1]
            current_macd = data['MACD'].iloc[-1]
            macd_signal = data['MACD'].rolling(window=9).mean().iloc[-1]
            
            # Combinar sinais
            final_signal = lstm_result["signal"]
            final_confidence = lstm_result["confidence"]
            
            # Ajustar baseado em RSI
            if current_rsi > 70 and final_signal == "CALL":
                final_confidence *= 0.7
            elif current_rsi < 30 and final_signal == "PUT":
                final_confidence *= 0.7
            
            # Ajustar baseado em MACD
            if (current_macd > macd_signal and final_signal == "PUT") or \
               (current_macd < macd_signal and final_signal == "CALL"):
                final_confidence *= 0.8
            
            # Calcular níveis de stop loss e take profit
            current_price = data['Close'].iloc[-1]
            atr = data['High'].subtract(data['Low']).rolling(window=14).mean().iloc[-1]
            
            if final_signal == "CALL":
                stop_loss = current_price - (atr * 1.5)
                take_profit = current_price + (atr * 2)
            elif final_signal == "PUT":
                stop_loss = current_price + (atr * 1.5)
                take_profit = current_price - (atr * 2)
            else:
                stop_loss = take_profit = None
            
            return {
                "symbol": symbol,
                "signal": final_signal,
                "confidence": round(final_confidence, 3),
                "entry_price": round(current_price, 4),
                "stop_loss": round(stop_loss, 4) if stop_loss else None,
                "take_profit": round(take_profit, 4) if take_profit else None,
                "strategy": "AI_Ensemble",
                "ai_models": ["LSTM"],
                "timestamp": datetime.utcnow().isoformat(),
                "market_conditions": {
                    "rsi": round(current_rsi, 2),
                    "macd": round(current_macd, 4),
                    "volume_trend": "high" if data['Volume'].iloc[-1] > data['Volume_SMA'].iloc[-1] else "low"
                }
            }
            
        except Exception as e:
            return {"error": f"Erro na análise de IA: {e}"}
    
    async def generate_ai_signals(self):
        """Gera sinais de IA para todos os símbolos suportados"""
        while self.is_running:
            try:
                # Analisar pares premium (requer licença)
                for symbol in settings.PREMIUM_PAIRS:
                    signal_data = await self.analyze_with_ai(symbol)
                    
                    if "error" not in signal_data and signal_data["signal"] != "HOLD":
                        await self.save_ai_signal(signal_data)
                        print(f"🤖 SINAL IA: {symbol} {signal_data['signal']} "
                              f"Conf: {signal_data['confidence']*100}%")
                
                # Analisar pares regulares
                regular_pairs = [p for p in settings.SUPPORTED_PAIRS if p not in settings.PREMIUM_PAIRS]
                for symbol in regular_pairs[:4]:  # Limitar para não sobrecarregar
                    signal_data = await self.analyze_with_ai(symbol)
                    
                    if "error" not in signal_data and signal_data["signal"] != "HOLD":
                        await self.save_ai_signal(signal_data)
                
                await asyncio.sleep(60)  # Analisar a cada minuto
                
            except Exception as e:
                print(f"Erro no serviço de IA: {e}")
                await asyncio.sleep(30)
    
    async def save_ai_signal(self, signal_data: Dict):
        """Salva sinal de IA no banco de dados"""
        async with AsyncSessionLocal() as db:
            signal = TradingSignal(
                pair=signal_data["symbol"],
                action=signal_data["signal"],
                confidence=signal_data["confidence"],
                entry_price=signal_data["entry_price"],
                stop_loss=signal_data["stop_loss"],
                take_profit=signal_data["take_profit"],
                timeframe="1h",
                broker="AI_System",
                strategy=signal_data["strategy"],
                is_ai_generated=True,
                is_premium=signal_data["symbol"] in settings.PREMIUM_PAIRS
            )
            db.add(signal)
            await db.commit()
    
    def start(self):
        """Inicia o serviço de IA"""
        if not self.is_running:
            self.is_running = True
            asyncio.create_task(self.initialize_models())
            asyncio.create_task(self.generate_ai_signals())
            print("🚀 Serviço de IA iniciado")
    
    def stop(self):
        """Para o serviço de IA"""
        self.is_running = False
        print("🛑 Serviço de IA parado")

ai_signal_service = AISignalService()
