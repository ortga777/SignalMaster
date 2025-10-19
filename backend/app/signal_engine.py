import asyncio
from app.market.fetcher import get_open_pairs, fetch_latest_price
from app.ws.manager import ws_broadcast_signal
from app.database import SessionLocal
from app import models
from datetime import datetime

# Simple engine config
POLL_INTERVAL = 5  # seconds between polls
MOMENTUM_WINDOW = 2  # number of samples to compare
THRESHOLD = 0.3  # price delta threshold to trigger signal (absolute)

async def run_signal_engine():
    print('🔔 Signal engine started (simple momentum)')
    history = {}
    while True:
        pairs = get_open_pairs()
        for p in pairs:
            data = fetch_latest_price(p)
            pair = data['pair']
            price = data['price']
            ts = data['ts']
            hist = history.setdefault(pair, [])
            hist.append((ts, price))
            # keep window length
            if len(hist) > MOMENTUM_WINDOW:
                hist.pop(0)
            # decide
            if len(hist) == MOMENTUM_WINDOW:
                old = hist[0][1]
                new = hist[-1][1]
                delta = new - old
                if abs(delta) >= THRESHOLD:
                    direction = 'CALL' if delta > 0 else 'PUT'
                    signal = {
                        'symbol': pair,
                        'platform': 'multi',
                        'direction': direction,
                        'confidence': min(99, int(abs(delta) * 100)),
                        'generated_at': datetime.utcnow().isoformat()
                    }
                    # persist signal
                    try:
                        db = SessionLocal()
                        s = models.Signal(symbol=signal['symbol'], platform=signal['platform'], direction=signal['direction'], confidence=signal['confidence'], payload={})
                        db.add(s); db.commit(); db.refresh(s)
                        db.close()
                    except Exception as e:
                        print('Error saving signal:', e)
                    # broadcast immediately
                    ws_broadcast_signal(signal)
                    print('Signal emitted:', signal)
        await asyncio.sleep(POLL_INTERVAL)
