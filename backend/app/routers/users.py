from fastapi import APIRouter, Body, HTTPException
from supabase_client import client
import yfinance as yf

router = APIRouter(prefix="/users", tags=["research"])


# returns the portfolio, the collection of assets, specific to the user
@router.get("/{id}/portfolio")  # more specific route must come first
def get_user_portfolio(id: int):
  response = client.table("portfolio").select("*").eq("user_id", id).execute()
  return {f"user #{id} portfolio": f"{response}"}


# simulates a trade by incrementing/decrementing the quantity of an asset, specific to the user
# trade must be a dictionary with the keys: "ticker" (str), "type" = "buy"/"sell" (str), "share_amount" (int)
@router.post("/{id}/trade")
def post_user_trade(id: int, trade: dict = Body(...)):

  # validate keys
  keys = {"ticker", "type", "share_amount"}
  if not keys.issubset(trade.keys()):
    raise HTTPException(status_code=400,
                        detail="Insufficient trade data provided")

  # validate type value as "buy" or "sell"
  if trade["type"] not in ["buy", "sell"]:
    raise HTTPException(status_code=400, detail="Invalid trade type provided")

  # validate share_amt as a positive integer"
  if not isinstance(trade["share_amount"], int) or trade["share_amount"] <= 0:
    raise HTTPException(status_code=400,
                        detail="Invalid share amount provided")

  # retrieve current price of the asset from yf
  price = yf.Ticker(trade["ticker"]).info["currentPrice"]
  print(f"current price of asset to trade {trade['ticker']}: {price}")

  # get the user's portfolio
  response = client.table("portfolio").select("*").eq("user_id", id).execute()
  assets = response.data or [
  ]  # assets is a list of dictionaries, each dict representing an asset

  # if the user wants to purchase an asset...
  if trade["type"] == "buy":
    # if the user already has the asset in their portfolio, increment the share amount and update the existing row
    if any(asset["ticker"] == trade["ticker"] for asset in assets):
      for asset in assets:
        if asset["ticker"] == trade["ticker"]:

          # average price needs to be updated upon a buy order
          new_avg = ((asset["share_amount"] * asset["average_price"]) + (
              trade["share_amount"] * price) )/ (asset["share_amount"] +
                                                trade["share_amount"])

          asset["share_amount"] += trade["share_amount"]
          client.table("portfolio").update({
              "share_amount":
              asset["share_amount"],
              "average_price":
              new_avg
          }).eq("id", asset["id"]).execute()
          return {
              "message":
              f"Bought {trade['share_amount']} shares of {trade['ticker']} with new average price {new_avg}"
          }
    else:
      # if the user does not have the asset in their portfolio, add a new row
      client.table("portfolio").insert({
          "user_id": id,
          "ticker": trade["ticker"],
          "share_amount": trade["share_amount"],
          "average_price": price
      }).execute()
      return {
          "message":
          f"Bought {trade['share_amount']} shares of {trade['ticker']} with new average price {price}"
      }

  # if the user wants to sell an asset...
  else:
    # if the user does not have the asset in their portfolio, raise an error
    if not any(asset["ticker"] == trade["ticker"] for asset in assets):
      raise HTTPException(
          status_code=400,
          detail="Cannot sell asset that does not exist in portfolio")
    else:
      # if the user has the asset in their portfolio, decrement the share amount and update the existing row
      for asset in assets:
        if asset["ticker"] == trade["ticker"]:
          if asset["share_amount"] < trade["share_amount"]:
            raise HTTPException(status_code=400,
                                detail="Cannot sell more shares than owned")
          else:
            # average price will remain the same upon a sell order
            asset["share_amount"] -= trade["share_amount"]
            client.table("portfolio").update({
                "share_amount":
                asset["share_amount"]
            }).eq("id", asset["id"]).execute()
            return {
                "message":
                f"Sold {trade['share_amount']} shares of {trade['ticker']}"
            }


# returns the specified user's data
@router.get("/{id}")
def get_user(id: int):
  response = client.table("users").select("*").eq("id", id).execute()
  return {f"user #{id} data": f"{response}"}
