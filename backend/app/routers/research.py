from fastapi import APIRouter
from ml.model_config import get_recs
import yfinance as yf

router = APIRouter(prefix="/research", tags=["research"])


@router.get("/{ticker}")
def get_ticker_info(ticker: str):
  info = yf.Ticker(ticker).info

  fields = [
      'currentPrice', 'longName', 'forwardPE', 'trailingPE', 'marketCap',
      'dividendYield', 'fiftyTwoWeekLow', 'fiftyTwoWeekHigh', 'sector',
      'industry', 'grossMargins', 'trailingEps', 'forwardEps', 'beta'
  ]
  msg = dict()

  for f in fields:
    try:
      msg[f] = info[f]
    except:
      msg[f] = None

  return {"ticker": ticker, "message": msg}


# provides a 1-year history of pricing data for the specified asset
@router.get("/{ticker}/history")
def get_ticker_history(ticker: str):
  hist = yf.Ticker(ticker).history(period="1y", interval="1d") # returns a df
  hist = hist.reset_index()  # preserve the date as a col
  hist['Date'] = hist['Date'].dt.strftime('%Y-%m-%d')  # remove time part
  time_data = hist.to_json(orient="records")
  return {"ticker": ticker, "message": time_data}


# intakes a dictionary of user input with keys: "sector", "marketCapLevel", "growthValueType", "forwardPE",
# returns a list of 5 recommended stocks 
@router.post("/recommendations")
def get_recommendations(user_input: dict):
  recs = get_recs(user_input)
  return {"message": recs}
