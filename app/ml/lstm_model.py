import os
import numpy as np
from typing import List

def predict_from_candles(candles: List[float]) -> float:
    """Faz predição baseada em candles"""
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
    """Inicializa o módulo ML"""
    print("ML module initialized")

# REMOVA ou comente a linha abaixo se existir:
# def build_dummy_model():  # ← Esta função não é mais usada
