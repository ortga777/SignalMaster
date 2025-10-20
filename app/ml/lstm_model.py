import os
import numpy as np
MODEL_PATH = os.getenv("MODEL_PATH", "/data/model/lstm_model.h5")

def build_dummy_model():
    # placeholder: real training should happen offline or in a background worker
    try:
        import tensorflow as tf
        from tensorflow.keras.models import Sequential
        from tensorflow.keras.layers import LSTM, Dense
        model = Sequential()
        model.add(LSTM(32, input_shape=(10,1)))
        model.add(Dense(1, activation='sigmoid'))
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        model.save(MODEL_PATH)
    except Exception as e:
        print("TensorFlow not available:", e)

def predict_from_candles(candles):
    # simple heuristic if no model
    try:
        if os.path.exists(MODEL_PATH):
            import tensorflow as tf
            model = tf.keras.models.load_model(MODEL_PATH)
            arr = np.array(candles[-10:]).reshape(1, -1)
            # transform to shape (1,10,1)
            arr = arr.reshape((1, arr.shape[1], 1))
            prob = float(model.predict(arr)[0][0])
            return prob
    except Exception as e:
        print("Model predict error:", e)
    # fallback heuristic: momentum
    if len(candles) < 3:
        return 0.5
    return float( (candles[-1] - candles[-2]) / (abs(candles[-2]) + 1e-9) * 0.5 + 0.5 )
