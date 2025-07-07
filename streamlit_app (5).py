
import streamlit as st
import pandas as pd

# Fare data
FARES = {
    "1-2": {"daily_cap": 8.90, "weekly_cap": 44.70},
    "1-3": {"daily_cap": 10.50, "weekly_cap": 52.50}
}

OYSTER_COST = 7.00

# Discounts
DISCOUNTS = {
    "Adult": 1.0,
    "11-15": 0.5,
    "Under 11": 0.0
}

st.title("London Transport Cost Comparison Tool")

# User inputs
days = st.slider("Number of travel days", 1, 14, 5)
passenger_type = st.selectbox("Passenger type", ["Adult", "11-15", "Under 11"])
zone = st.selectbox("Zones", ["1-2", "1-3"])
payment_method = st.selectbox("Payment method", ["Contactless", "Oyster", "Smartcard"])
start_day = st.selectbox("Start day of travel", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])

# Calculate cost
def calculate_cost(days, passenger_type, zone, payment_method, start_day):
    if passenger_type == "Under 11":
        return 0.0, "Free travel for Under 11"

    discount = DISCOUNTS[passenger_type]
    daily_cap = FARES[zone]["daily_cap"] * discount
    weekly_cap = FARES[zone]["weekly_cap"] * discount

    if payment_method == "Contactless":
        if start_day != "Monday":
            if days > 7:
                cost = weekly_cap + (days - 7) * daily_cap
            else:
                cost = min(days * daily_cap, weekly_cap)
            note = "Contactless weekly cap applies only if travel starts on Monday"
        else:
            if days > 7:
                cost = weekly_cap + (days - 7) * daily_cap
            else:
                cost = min(days * daily_cap, weekly_cap)
            note = "Weekly cap applied (Mon-Sun)"
    else:
        if days > 7:
            cost = weekly_cap + (days - 7) * daily_cap
            note = "Weekly cap + daily caps for extra days"
        elif days >= 5:
            cost = min(days * daily_cap, weekly_cap)
            note = "Weekly cap may be more cost-effective"
        else:
            cost = days * daily_cap
            note = "Daily caps applied"

        if payment_method == "Oyster":
            cost += OYSTER_COST
            note += " (includes £7 Oyster card cost)"

    return round(cost, 2), note

# Compute and display result
total_cost, recommendation = calculate_cost(days, passenger_type, zone, payment_method, start_day)
st.subheader(f"Estimated Total Cost: £{total_cost}")
st.caption(recommendation)
