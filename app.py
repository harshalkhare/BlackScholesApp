from flask import Flask, render_template, request, jsonify
from datetime import datetime, time
from BlackScholes.LTP import fetch_ltp, Interval
from BlackScholes.BlackScholesModel import black_scholes
from BlackScholes.FixedInputs import *  # includes r, WE*, SE*, ME*
from BlackScholes.SensibullFunctions import get_atm_strike_by_expiry, get_atm_iv_by_expiry

app = Flask(__name__)

def calculate_prices(expiry_key):
    # Map dropdown key → expiry variables
    expiries = {
        "weekly": (WE2, WE3, WE),
        "second_weekly": (SE2, SE3, SE),
        "monthly": (ME2, ME3, ME)
    }

    expiry_iso, expiry_display, expiry_code = expiries[expiry_key]

    # Time to expiry
    expiry_date = datetime.strptime(expiry_display, "%d-%m-%Y")
    expiry_time = datetime.combine(expiry_date, time(15, 30))
    T_hours = (expiry_time - datetime.now()).total_seconds() / 3600

    Stock = "NIFTY"
    Exchange = "NSE"

    # ATM strike + IV
    strike = get_atm_strike_by_expiry(Stock, expiry_iso)
    strike_str = str(int(strike)) if strike == int(strike) else str(strike)
    sigma = get_atm_iv_by_expiry(Stock, expiry_iso)

    # Option symbols
    callstrike = f"{Stock}{expiry_code}C{strike_str}"
    putstrike = f"{Stock}{expiry_code}P{strike_str}"

    # LTPs
    S = fetch_ltp(Stock, Exchange, Interval.in_1_minute)
    actual_put_price = fetch_ltp(putstrike, "NSE", Interval.in_1_minute)
    actual_call_price = fetch_ltp(callstrike, "NSE", Interval.in_1_minute)

    # Theoretical prices
    predicted_put_price = black_scholes(S, strike, T_hours, r, sigma, option_type="put")
    predicted_call_price = black_scholes(S, strike, T_hours, r, sigma, option_type="call")

    return {
        "expiry": expiry_key.replace("_", " ").title(),
        "expiry_date": expiry_display,
        "strike": strike_str,
        "iv": round(sigma, 4),
        "spot": S,
        "predicted_put": round(predicted_put_price, 2),
        "actual_put": round(actual_put_price, 2),
        "diff_put": round(predicted_put_price - actual_put_price, 2),
        "predicted_call": round(predicted_call_price, 2),
        "actual_call": round(actual_call_price, 2),
        "diff_call": round(predicted_call_price - actual_call_price, 2),
    }


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/data")
def api_data():
    expiry = request.args.get("expiry", "weekly")  # default = weekly
    result = calculate_prices(expiry)
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
