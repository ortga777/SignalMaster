import os
import numpy as np
from typing import List

MODEL_PATH = os.getenv("MODEL_PATH", "./data/model/lstm_model.h5")

def predict_from_candles(candles: List[float]) -> float:
    """
    Faz predição baseada em candles (versão sem TensorFlow)
    Retorna probabilidade entre 0 e 1
    """
    return simple_momentum_prediction(candles)

def simple_momentum_prediction(candles: List[float]) -> float:
    """Predição simples baseada em momentum"""
    if len(candles) < 2:
        return 0.5
    
    current = candles[-1]
    previous = candles[-2]
    
    if previous == 0:
        return 0.5
    
    momentum = (current - previous) / abs(previous)
    probability = 0.5 + (momentum * 2.5)
    
    return max(0.1, min(0.9, probability))

def initialize_model_if_needed():
    """Função placeholder para compatibilidade"""
    print("ML module initialized (heuristic mode)")
