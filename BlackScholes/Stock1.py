from LTP import * # To fetch LTP from tradingView
from BlackScholesModel import black_scholes # BlackScholes Model
from datetime import *
import numpy as np
from FixedInputs import * #RiskFreeRate & Expires
from  SensibullFunctions import *

# Time Left to Expiry
expiry_date = datetime.strptime(ME3, "%d-%m-%Y")
expiry_time = datetime.combine(expiry_date, time(15, 30))  # Expiry at 3:30 PM IST
T_hours = (expiry_time - datetime.now()).total_seconds() / 3600  # Convert to hours

# Inputs
Stock = "HDFCBANK"
Exchange = "NSE"

strike = get_atm_strike_by_expiry(Stock, ME2) # StrikePrice
strike_str = str(int(strike)) if strike == int(strike) else str(strike) #Converts Decimal and string as required

callstrike = f"{Stock}{ME}C{strike_str}" #IREDA250626C170
putstrike = f"{Stock}{ME}P{strike_str}" #IREDA250626P170
sigma = get_atm_iv_by_expiry(Stock, ME2) #0.362158

print(f"ATM Strike {strike_str} : IV {sigma}")


S = fetch_ltp(Stock, Exchange, Interval.in_1_minute)
K = float(strike)

predicted_put_price = black_scholes(S, K, T_hours, r, sigma, option_type="put")
actual_put_price = fetch_ltp(putstrike, "NSE", Interval.in_1_minute)
predicted_call_price = black_scholes(S, K, T_hours, r, sigma, option_type="call")
actual_call_price = fetch_ltp(callstrike, "NSE", Interval.in_1_minute)



print(f"Predicted PUT Option Price: {predicted_put_price:.2f}")
print(f"Actual Put Option Price: {actual_put_price:.2f}")
print(f"Difference (Put): {(RED if predicted_put_price - actual_put_price > 0 else GREEN)}{predicted_put_price - actual_put_price:.2f}{RESET}")
print("=======================================")
print(f"Predicted CALL Option Price: {predicted_call_price:.2f}")
print(f"Actual Call Option Price: {actual_call_price:.2f}")
print(f"Difference (Call): {(GREEN if predicted_call_price - actual_call_price > 0 else RED)}{predicted_call_price - actual_call_price:.2f}{RESET}")
