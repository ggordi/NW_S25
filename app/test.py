import yfinance as yf

ticker = "MSFT"

# info = yf.Ticker(ticker).info
# msg = {'currentPrice': info['currentPrice'], 'forwardPE': info['forwardPE'], 'trailingPE': info['trailingPE'], 'marketCap': info['marketCap'], 'dividendYield': info['dividendYield'], 'fiftyTwoWeekLow': info['fiftyTwoWeekLow'], 'fiftyTwoWeekHigh': info['fiftyTwoWeekHigh'], 'sector': info['sector'], 'industry': info['industry'], 'grossMargins': info['grossMargins'], 'trailingEps': info['trailingEps'], 'forwardEps': info['forwardEps'], 'beta': info['beta']}

# fields = ['currentPrice', 'forwardPE', 'trailingPE', 'marketCap', 'dividendYield', 'fiftyTwoWeekLow', 'fiftyTwoWeekHigh', 'sector', 'industry', 'grossMargins', 'trailingEps', 'forwardEps', 'beta']
# msg = dict()

# for f in fields:
#   msg[f] = info[f]

# print(msg)

hist = yf.Ticker(ticker).history(period="1y", interval="1d") # returns a df
hist = hist.reset_index()  # preserve the date as a col
hist['Date'] = hist['Date'].dt.strftime('%Y-%m-%d')  # remove time part
print(hist.to_json(orient="records"))

