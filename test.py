import yfinance as yf

import json

print(yf.Ticker("TSM").info["longBusinessSummary"])

# with open("sample.json", "w") as outfile:
#     outfile.write(json.dumps(yf.Ticker("aapl").info))

