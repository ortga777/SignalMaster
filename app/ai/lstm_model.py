import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from sklearn.preprocessing import MinMaxScaler
import joblib
import yfinance as yf
from datetime import datetime, timedelta
import os
from app.core.config import settings

class LSTMPredictor:
    def __init__(self):
        self.model = None
        self.scaler = MinMaxScaler()
        self.sequence_length = 60
        self.model_path = os.path.join(settings.AI_MODEL_PATH, settings.LSTM_MODEL_FILE)
        self.scaler_path = os.path.join(settings.AI_MODEL_PATH, "scaler.pkl")
        
    async def prepare_data(self, symbol: str, period: str = "2y") -> pd.DataFrame:
        """Prepara dados para treinamento do modelo"""
        try:
            # Buscar dados históricos
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period, interval="1h")
            
            if data.empty:
                print(f"Dados não encontrados para {symbol}")
                return None
            
            # Preparar features
            data = data[['Open', 'High', 'Low', 'Close', 'Volume']]
            
            # Adicionar indicadores técnicos
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
            data['MACD_Signal'] = data['MACD'].ewm(span=9).mean()
            
            # Volatilidade
            data['Volatility'] = data['Close'].rolling(window=20).std()
            
            # Remover NaN
            data = data.dropna()
            
            return data
            
        except Exception as e:
            print(f"Erro ao preparar dados: {e}")
            return None
    
    def create_sequences(self, data: pd.DataFrame) -> tuple:
        """Cria sequências para o modelo LSTM"""
        feature_columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'SMA_20', 'SMA_50', 
                          'EMA_12', 'EMA_26', 'RSI', 'MACD', 'MACD_Signal', 'Volatility']
        
        # Normalizar dados
        scaled_data = self.scaler.fit_transform(data[feature_columns])
        
        X, y = [], []
        
        for i in range(self.sequence_length, len(scaled_data)):
            X.append(scaled_data[i-self.sequence_length:i])
            y.append(scaled_data[i, 3])  # Prever preço de fechamento
        
        return np.array(X), np.array(y)
    
    def build_model(self, input_shape: tuple) -> Sequential:
        """Constrói o modelo LSTM"""
        model = Sequential([
            LSTM(50, return_sequences=True, input_shape=input_shape),
            Dropout(0.2),
            LSTM(50, return_sequences=True),
            Dropout(0.2),
            LSTM(50),
            Dropout(0.2),
            Dense(25),
            Dense(1)
        ])
        
        model.compile(optimizer=Adam(learning_rate=0.001), loss='mse', metrics=['mae'])
        return model
    
    async def train_model(self, symbol: str) -> bool:
        """Treina o modelo LSTM"""
        try:
            data = await self.prepare_data(symbol)
            if data is None:
                return False
            
            X, y = self.create_sequences(data)
            
            if len(X) == 0:
                return False
            
            # Dividir dados
            split = int(0.8 * len(X))
            X_train, X_test = X[:split], X[split:]
            y_train, y_test = y[:split], y[split:]
            
            # Construir e treinar modelo
            self.model = self.build_model((X.shape[1], X.shape[2]))
            
            history = self.model.fit(
                X_train, y_train,
                validation_data=(X_test, y_test),
                epochs=50,
                batch_size=32,
                verbose=0
            )
            
            # Salvar modelo e scaler
            os.makedirs(settings.AI_MODEL_PATH, exist_ok=True)
            self.model.save(self.model_path)
            joblib.dump(self.scaler, self.scaler_path)
            
            print(f"✅ Modelo LSTM treinado para {symbol}")
            return True
            
        except Exception as e:
            print(f"❌ Erro no treinamento: {e}")
            return False
    
    async def load_model(self) -> bool:
        """Carrega modelo treinado"""
        try:
            if os.path.exists(self.model_path) and os.path.exists(self.scaler_path):
                self.model = load_model(self.model_path)
                self.scaler = joblib.load(self.scaler_path)
                return True
            return False
        except Exception as e:
            print(f"Erro ao carregar modelo: {e}")
            return False
    
    async def predict(self, data: pd.DataFrame) -> dict:
        """Faz previsão usando o modelo LSTM"""
        if self.model is None:
            await self.load_model()
        
        if self.model is None:
            return {"error": "Modelo não carregado"}
        
        try:
            # Preparar dados para previsão
            feature_columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'SMA_20', 'SMA_50', 
                              'EMA_12', 'EMA_26', 'RSI', 'MACD', 'MACD_Signal', 'Volatility']
            
            # Garantir que temos dados suficientes
            if len(data) < self.sequence_length:
                return {"error": "Dados insuficientes para previsão"}
            
            # Selecionar últimas sequências
            recent_data = data[feature_columns].tail(self.sequence_length)
            scaled_data = self.scaler.transform(recent_data)
            
            # Fazer previsão
            X = np.array([scaled_data])
            prediction = self.model.predict(X, verbose=0)
            
            # Reverter escala
            dummy = np.zeros((1, len(feature_columns)))
            dummy[0, 3] = prediction[0, 0]  # Coluna do preço de fechamento
            predicted_price = self.scaler.inverse_transform(dummy)[0, 3]
            
            current_price = data['Close'].iloc[-1]
            price_change = ((predicted_price - current_price) / current_price) * 100
            
            # Gerar sinal baseado na previsão
            if price_change > 0.5:
                signal = "CALL"
                confidence = min(0.95, abs(price_change) / 10)
            elif price_change < -0.5:
                signal = "PUT"
                confidence = min(0.95, abs(price_change) / 10)
            else:
                signal = "HOLD"
                confidence = 0.0
            
            return {
                "signal": signal,
                "confidence": round(confidence, 3),
                "predicted_price": round(predicted_price, 4),
                "current_price": round(current_price, 4),
                "price_change_percent": round(price_change, 2),
                "model": "LSTM",
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {"error": f"Erro na previsão: {e}"}

lstm_predictor = LSTMPredictor()
