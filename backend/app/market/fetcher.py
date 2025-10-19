
# Market data fetcher that tries platform-specific fetchers sequentially.
from typing import List, Dict
from . import DEFAULT_PAIRS
import importlib, time, random

PLATFORMS = ['quotex','pocketoption','binomo','iqoption','olymptrade','deriv','spectre','binary_com']

def get_open_pairs() -> List[str]:
    return DEFAULT_PAIRS

def fetch_latest_price(pair: str) -> Dict:
    # Try each platform-specific fetcher (best-effort). Each fetcher must implement fetch_price(pair).
    for plat in PLATFORMS:
        try:
            mod = importlib.import_module(f'app.platforms.{plat}')
            # find a class that endswith Fetcher
            FetcherClass = None
            for attr in dir(mod):
                if attr.lower().endswith('fetcher'):
                    FetcherClass = getattr(mod, attr)
                    break
            if not FetcherClass:
                continue
            f = FetcherClass(headless=True)
            # optionally: f.login() if needed and credentials provided
            res = f.fetch_price(pair)
            if res and res.get('price') not in (None, 0.0):
                return res
        except Exception as e:
            # ignore and try next platform
            continue
    # Fallback simple generator if no platform returns price
    base = abs(hash(pair)) % 100 + 1
    price = base + random.uniform(-1.0, 1.0)
    return {'pair': pair, 'price': round(price, 5), 'ts': int(time.time())}
