# Bybit Smart Micro Bot
Concept-stage Python trading bot for Bybit featuring a Tkinter GUI, learning and live modes, risk controls, and real-time trade analytics.

## ⚠️ IMPORTANT DISCLAIMER

**This project is experimental and NOT production-ready. Use for educational purposes only.**

### Security & Test Data Notice

- **ALL API KEYS** in this repository are **TEST KEYS** from demo/paper trading accounts
- **ALL TRADE LOGS** are proof-of-concept data for demonstration purposes only
- **ALL CONFIGURATION FILES** contain placeholder values and must be replaced

### Before Using This Bot:

1. **NEVER use the API keys found in this code** - they are public test keys
2. **Replace ALL credentials** with your own secure keys
3. **Implement proper API security**:
   - Use environment variables (`.env` file)
   - Never hardcode credentials in source code
   - Add `.env` to your `.gitignore`
   - Use API keys with minimal required permissions
4. **Generate your own trading data** - existing logs are examples only
5. **Test thoroughly** on paper trading accounts before risking real funds

### Proper API Key Setup:
```python
# ❌ DO NOT DO THIS (how test keys are shown in this repo):
API_KEY = "test_key_here"

# ✅ DO THIS instead:
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("BYBIT_API_KEY")
API_SECRET = os.getenv("BYBIT_API_SECRET")
```

Create a `.env` file (never commit this):
```
BYBIT_API_KEY=your_actual_key
BYBIT_API_SECRET=your_actual_secret
```

## No Warranty

This software is provided "as is" without warranty of any kind. Trading cryptocurrencies carries significant financial risk. The authors are not responsible for any financial losses incurred through use of this software.


