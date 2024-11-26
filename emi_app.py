"""
Interactive EMI Calculator with House Price
This app calculates the Equated Monthly Installment (EMI) for a home 
loan based on the loan amount, interest rate, and tenure. You can also 
adjust the house price and loan-to-house price ratio to calculate the 
loan amount.
"""

import math

import streamlit as st
import plotly.graph_objects as go

LAKH = 100000  # ₹1,00,000
CRORE = 10000000  # ₹1,00,00,000


def calculate_emi(principal: int, annual_rate: float, tenure_years: int) -> float:
    """
    Calculate the Equated Monthly Installment (EMI) for a loan.

    Args:
        principal (int): Loan amount in INR
        annual_rate (float): Annual interest rate in percentage
        tenure_years (int)): Loan tenure in years

    Returns:
        float: EMI value in INR
    """
    monthly_rate = annual_rate / (12 * 100)  # Convert annual rate to monthly rate
    tenure_months = tenure_years * 12  # Convert years to months
    emi = (
        principal
        * monthly_rate
        * (1 + monthly_rate) ** tenure_months
        / ((1 + monthly_rate) ** tenure_months - 1)
    )
    return emi


def generate_emi_data(principal: int, annual_rate: float) -> tuple:
    """
    Generate EMI data for different loan tenures.

    Args:
        principal (int): Loan amount in INR
        annual_rate (float): Annual interest rate in percentage

    Returns:
        tuple: A tuple containing tenures and corresponding EMI values
    """
    tenures = list(range(2, 31))  # Loan tenure from 1 to 30 years
    emis = [calculate_emi(principal, annual_rate, tenure) for tenure in tenures]
    return tenures, emis


def format_indian_currency(value):
    """Format numbers to Indian currency style with lakhs and crores."""
    if value >= 1e7:
        return f"{value / 1e7:.2f} Cr"
    elif value >= 1e5:
        return f"{value / 1e5:.2f} L"
    else:
        return f"{value / 1e3:.2f} K"


# Streamlit app
st.title("Interactive EMI Calculator with House Price")

# House price and loan ratio
st.sidebar.header("Property and Loan Details")
# house_price = st.sidebar.number_input(
#     "House Price (₹)",
#     min_value=2 * CRORE,
#     max_value=10 * CRORE,
#     step=10 * LAKH,
#     value=3 * CRORE,
# )

house_price = st.sidebar.slider(
    "House Price (₹)",
    min_value=2 * CRORE,
    max_value=10 * CRORE,
    step=20 * LAKH,
    value=3 * CRORE,
)
# house_price = house_price_slider if house_price_slider != house_price else house_price

loan_ratio = st.sidebar.slider(
    "Loan-to-House Price Ratio (%)", min_value=10, max_value=100, step=5, value=80
)

# Calculate loan amount based on ratio
calculated_loan_amount = house_price * (loan_ratio / 100)
st.sidebar.write(
    f"\nDown Payment : ₹{format_indian_currency(house_price - calculated_loan_amount)}"
)
st.sidebar.write(
    f"Calculated Loan Amount: ₹{format_indian_currency(calculated_loan_amount)}"
)

# Loan amount and interest rate inputs
principal = st.sidebar.number_input(
    "Loan Amount (₹)",
    min_value=50 * LAKH,
    max_value=10 * CRORE,
    step=10 * LAKH,
    value=int(calculated_loan_amount),
)
# principal_slider = st.sidebar.slider(
#     "Adjust Loan Amount",
#     min_value=50 * LAKH,
#     max_value=10 * CRORE,
#     step=10 * LAKH,
#     value=principal,
# )
# principal = principal_slider if principal_slider != principal else principal

annual_rate = st.sidebar.number_input(
    "Annual Interest Rate (%)", min_value=5.0, max_value=15.0, step=0.1, value=8.5
)
annual_rate_slider = st.sidebar.slider(
    "Adjust Interest Rate", min_value=5.0, max_value=15.0, step=0.1, value=annual_rate
)
annual_rate = annual_rate_slider if annual_rate_slider != annual_rate else annual_rate

# Generate data
tenures, emis = generate_emi_data(principal, annual_rate)

# Interactive plot
fig = go.Figure()
fig.add_trace(go.Scatter(x=tenures, y=emis, mode="lines+markers", name="EMI"))

# Format Y-axis for Indian numbering
Y_AXIS_TICKS = [i * 1e5 for i in range(1, math.ceil(max(emis) / 1e5) + 1)]
fig.update_layout(
    title="EMI vs Loan Tenure",
    xaxis_title="Loan Tenure (Years)",
    yaxis_title="Monthly EMI (₹)",
    template="plotly_white",
    hovermode="x unified",
    yaxis=dict(
        tickformat="~s",
        # tickvals are multiple of 1 lakh
        tickvals=Y_AXIS_TICKS,
        ticktext=[format_indian_currency(val) for val in Y_AXIS_TICKS],
    ),
)

# Display values and graph
st.write(
    f"### House Price: ₹{format_indian_currency(house_price)}, Loan-to-House Price Ratio: {loan_ratio}%"
)
st.write(
    f"### Loan Amount: ₹{format_indian_currency(principal)}, Annual Interest Rate: {annual_rate}%"
)
st.plotly_chart(fig, use_container_width=True)
