import yfinance as yf

import json

print(yf.Ticker("TSM").info["longBusinessSummary"])


from app import show_fsm

show_fsm()

# with open("sample.json", "w") as outfile:
#     outfile.write(json.dumps(yf.Ticker("aapl").info))

