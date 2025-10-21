here# No SignalBase, mude:
class SignalBase(BaseModel):
    symbol: str
    signal_type: SignalType
    confidence: float = 0.5
    price: float
    time_frame: str = "1h"
    signal_data: Optional[dict] = None  # Mude de 'metadata' para 'signal_data'
