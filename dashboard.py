import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# Title of the app
st.title("Palantir Financial Analysis Dashboard")

# Fetch data
pltr = yf.Ticker("PLTR")
historical_data = pltr.history(period="max")
financials = pltr.financials
balance_sheet = pltr.balance_sheet
cash_flow = pltr.cashflow

# ------------------------------------------------------------------------------------
# 1. Historical Data
# ------------------------------------------------------------------------------------
st.subheader("Historical Stock Prices")
st.line_chart(historical_data['Close'])

# ------------------------------------------------------------------------------------
# 2. Financial Ratios
# ------------------------------------------------------------------------------------
st.subheader("Financial Ratios")

# Profitability Ratios
revenue = financials.loc['Total Revenue']
net_income = financials.loc['Net Income']
gross_profit = financials.loc['Gross Profit']
shareholder_equity = balance_sheet.loc['Stockholders Equity']

gross_profit_margin = (gross_profit / revenue) * 100
net_profit_margin = (net_income / revenue) * 100
roe = (net_income / shareholder_equity) * 100

# Liquidity Ratios
current_assets = balance_sheet.loc['Current Assets']
current_liabilities = balance_sheet.loc['Current Liabilities']
inventory = balance_sheet.loc['Inventory'] if 'Inventory' in balance_sheet.index else 0

current_ratio = current_assets / current_liabilities
quick_ratio = (current_assets - inventory) / current_liabilities

# Efficiency Ratios
total_assets = balance_sheet.loc['Total Assets']
receivables = balance_sheet.loc['Accounts Receivable']

asset_turnover = revenue / total_assets
receivables_turnover = revenue / receivables

# Leverage Ratios
total_liabilities = balance_sheet.loc['Total Liabilities Net Minority Interest']
ebit = financials.loc['EBIT']
interest_expense = financials.loc['Interest Expense']

debt_to_equity = total_liabilities / shareholder_equity
interest_coverage = ebit / interest_expense

# Market Ratios
market_cap = pltr.info['marketCap']
book_value = shareholder_equity.iloc[0]
shares_outstanding = pltr.info['sharesOutstanding']

pe_ratio = market_cap / net_income.iloc[0]
pb_ratio = market_cap / book_value

# Display Ratios
st.write("### Profitability Ratios")
st.write(f"Gross Profit Margin: {gross_profit_margin.iloc[0]:.2f}%")
st.write(f"Net Profit Margin: {net_profit_margin.iloc[0]:.2f}%")
st.write(f"Return on Equity (ROE): {roe.iloc[0]:.2f}%")

st.write("### Liquidity Ratios")
st.write(f"Current Ratio: {current_ratio.iloc[0]:.2f}")
st.write(f"Quick Ratio: {quick_ratio.iloc[0]:.2f}")

st.write("### Efficiency Ratios")
st.write(f"Asset Turnover: {asset_turnover.iloc[0]:.2f}")
st.write(f"Receivables Turnover: {receivables_turnover.iloc[0]:.2f}")

st.write("### Leverage Ratios")
st.write(f"Debt-to-Equity Ratio: {debt_to_equity.iloc[0]:.2f}")
st.write(f"Interest Coverage Ratio: {interest_coverage.iloc[0]:.2f}")

st.write("### Market Ratios")
st.write(f"P/E Ratio: {pe_ratio:.2f}")
st.write(f"Price-to-Book (P/B) Ratio: {pb_ratio:.2f}")

# ------------------------------------------------------------------------------------
# 3. Candlestick Charts with Moving Averages and Volume
# ------------------------------------------------------------------------------------
st.subheader("Candlestick Chart with Moving Averages")

# Calculate moving averages
historical_data['MA_50'] = historical_data['Close'].rolling(window=50).mean()
historical_data['MA_200'] = historical_data['Close'].rolling(window=200).mean()

# Create a candlestick chart
candlestick = go.Figure(data=[go.Candlestick(
    x=historical_data.index,
    open=historical_data['Open'],
    high=historical_data['High'],
    low=historical_data['Low'],
    close=historical_data['Close']
)])

# Add moving averages
candlestick.add_trace(go.Scatter(x=historical_data.index, y=historical_data['MA_50'], name="50-Day MA", line=dict(color='orange')))
candlestick.add_trace(go.Scatter(x=historical_data.index, y=historical_data['MA_200'], name="200-Day MA", line=dict(color='green')))

# Update layout
candlestick.update_layout(
    title="Palantir Candlestick Chart with Moving Averages",
    xaxis_title="Date",
    yaxis_title="Price (USD)"
)

# Display the chart
st.plotly_chart(candlestick)

# ------------------------------------------------------------------------------------
# 4. Market Comparison with S&P 500
# ------------------------------------------------------------------------------------
st.subheader("Palantir vs. S&P 500 Performance (Since September 30, 2020)")

# Fetch S&P 500 data
sp500 = yf.Ticker("^GSPC")
sp500_data = sp500.history(period="max")

# Filter data from September 30, 2020
start_date = "2020-09-30"
historical_data = historical_data.loc[start_date:]
sp500_data = sp500_data.loc[start_date:]

# Normalize prices to compare performance
historical_data['Normalized Close'] = historical_data['Close'] / historical_data['Close'].iloc[0]
sp500_data['Normalized Close'] = sp500_data['Close'] / sp500_data['Close'].iloc[0]

# Combine data into a single DataFrame
comparison_data = pd.DataFrame({
    "Date": historical_data.index,
    "Palantir (PLTR)": historical_data['Normalized Close'],
    "S&P 500": sp500_data['Normalized Close']
})

# Create an interactive line plot
fig = px.line(comparison_data, x="Date", y=["Palantir (PLTR)", "S&P 500"],
              title="Palantir vs. S&P 500 Performance (Since September 30, 2020)",
              labels={"value": "Normalized Price", "variable": "Index"})

# Display the plot
st.plotly_chart(fig)

# ------------------------------------------------------------------------------------
# 5. DCF Valuation
# ------------------------------------------------------------------------------------
st.subheader("Discounted Cash Flow (DCF) Valuation")

# Fetch free cash flow data
free_cash_flow = cash_flow.loc['Free Cash Flow']

# Assumptions
discount_rate = st.number_input("Discount Rate (%)", value=10.0) / 100
growth_rate = st.number_input("Growth Rate (%)", value=5.0) / 100
years = st.number_input("Forecast Period (Years)", value=5)

# Calculate free cash flows for the forecast period
forecasted_fcf = []
for t in range(1, years + 1):
    fcf = free_cash_flow.iloc[0] * (1 + growth_rate) ** t
    forecasted_fcf.append(fcf)

# Calculate terminal value
terminal_value = forecasted_fcf[-1] * (1 + growth_rate) / (discount_rate - growth_rate)

# Discount cash flows
dcf_value = 0
for t, fcf in enumerate(forecasted_fcf, start=1):
    dcf_value += fcf / (1 + discount_rate) ** t

# Add terminal value
dcf_value += terminal_value / (1 + discount_rate) ** years

# Display DCF value
st.write(f"Discounted Cash Flow (DCF) Value: ${dcf_value / 1e9:.2f} Billion")

# ------------------------------------------------------------------------------------
# 6. Stock Price Prediction
# ------------------------------------------------------------------------------------
st.subheader("Stock Price Prediction")

# Prepare data for machine learning
historical_data['Returns'] = historical_data['Close'].pct_change()
historical_data = historical_data.dropna()
X = historical_data[['Open', 'High', 'Low', 'Volume']]
y = historical_data['Close']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions
predictions = model.predict(X_test)

# Display evaluation metrics
mse = mean_squared_error(y_test, predictions)
r2 = r2_score(y_test, predictions)
st.write(f"Mean Squared Error: {mse:.2f}")
st.write(f"R-squared: {r2:.2f}")

# Plot actual vs predicted prices
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(y_test, predictions, color='blue', label="Predictions")
ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], color='red', linestyle='--', label="Ideal Line")
ax.set_xlabel("Actual Prices")
ax.set_ylabel("Predicted Prices")
ax.set_title("Actual vs Predicted Prices")
ax.legend()
ax.grid()
st.pyplot(fig)

# ------------------------------------------------------------------------------------
# 7. Personal Investment
# ------------------------------------------------------------------------------------
st.subheader("My Investment in Palantir")

# Define investment details
purchase_price = 6.89  # My purchase price
purchase_date = "2022-05-11"  # My purchase date
current_price = historical_data['Close'].iloc[-1]  # Latest closing price
roi = ((current_price - purchase_price) / purchase_price) * 100  # Calculate ROI

# Display investment details
st.write(f"Purchased at: ${purchase_price} on {purchase_date}")
st.write(f"Current Price: ${current_price:.2f}")
st.write(f"ROI: {roi:.2f}%")

# Plot investment performance
investment_data = historical_data.loc[purchase_date:]
st.line_chart(investment_data['Close'])

# ------------------------------------------------------------------------------------
# Additional Analysis
# ------------------------------------------------------------------------------------
st.subheader("SWOT Analysis")

# Display SWOT Analysis
st.write("""
### Strengths
1. **Strong Government Contracts:** Palantir has long-standing relationships with government agencies, providing a stable revenue stream.
2. **Advanced Data Analytics:** The company’s platforms (e.g., Foundry, Gotham) are highly sophisticated and tailored for complex data analysis.
3. **High Barriers to Entry:** Palantir’s proprietary technology and expertise create significant barriers for competitors.

### Weaknesses
1. **Dependence on Government Contracts:** A large portion of revenue comes from government contracts, making the company vulnerable to policy changes.
2. **High Customer Acquisition Costs:** Acquiring new clients is expensive and time-consuming.
3. **Limited Profitability:** Palantir has struggled to achieve consistent profitability.

### Opportunities
1. **Expansion into Commercial Markets:** There is significant potential for growth in industries like healthcare, finance, and manufacturing.
2. **International Growth:** Palantir can expand its presence in international markets.
3. **AI and Machine Learning Integration:** Leveraging AI/ML can enhance its platforms and attract more clients.

### Threats
1. **Competition:** Competitors like Snowflake and Microsoft are entering the data analytics space.
2. **Regulatory Risks:** Increased scrutiny on data privacy and security could impact operations.
3. **Economic Downturns:** Reduced spending by governments and enterprises during economic downturns could hurt revenue.
""")

st.subheader("Conclusion")

# Display Conclusion
st.write("""
Palantir Technologies (PLTR) is a unique player in the data analytics space, with a strong focus on government contracts and complex data solutions. While the company has demonstrated significant strengths, such as its advanced technology and high barriers to entry, it also faces challenges like dependence on government revenue and limited profitability.

The financial analysis highlights Palantir’s potential for growth, particularly in commercial markets and international expansion. However, risks such as competition, regulatory changes, and economic downturns must be carefully managed.

From an investment perspective, Palantir’s stock has shown volatility, but its long-term potential remains promising, especially if it can diversify its revenue streams and achieve consistent profitability. Investors should closely monitor the company’s ability to execute its growth strategies and adapt to market changes.
""")