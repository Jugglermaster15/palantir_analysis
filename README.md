# palantir_analysis
Financial Analysis of Palantir
# Palantir Financial Analysis Project

## Overview
This project provides a comprehensive financial analysis of Palantir Technologies (PLTR), including:
- Historical stock prices.
- Financial ratios (e.g., gross profit margin, debt-to-equity ratio).
- Candlestick charts with moving averages and volume.
- Interactive comparison of Palantir's performance with the S&P 500 since September 30, 2020.
- Discounted Cash Flow (DCF) valuation.
- Stock price prediction using machine learning.
- Market share comparison against top 9 competitors (Public).
- Personal investment performance tracking.
- SWOT analysis and conclusion.

## Features
1. **Historical Data:** Fetches and displays Palantir's stock prices.
2. **Financial Ratios:** Calculates key financial metrics.
   - **Profitability Ratios:** Gross Profit Margin, Net Profit Margin, Return on Equity (ROE).
   - **Liquidity Ratios:** Current Ratio, Quick Ratio.
   - **Efficiency Ratios:** Asset Turnover, Receivables Turnover.
   - **Leverage Ratios:** Debt-to-Equity Ratio, Interest Coverage Ratio.
   - **Market Ratios:** P/E Ratio, Price-to-Book (P/B) Ratio.
3. **Candlestick Charts:** Visualizes stock price movements with 50-day and 200-day moving averages.
4. **Market Comparison:** Interactive comparison of Palantir's performance with the S&P 500 since September 30, 2020.
5. **DCF Valuation:** Estimates Palantir's intrinsic value using the Discounted Cash Flow method.
6. **Stock Price Prediction:** Predicts closing prices using a linear regression model.
7. **Market Share Comparison:** Compares the actual market share of Palantir against other top 9 competitors in the field (Public companies).
8. **Personal Investment:** Tracks ROI based on a purchase price of $6.89 on May 11, 2022.
9. **Additional Analysis:** Includes a SWOT analysis and conclusion.

## Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/Jugglermaster15/Palantir_Analysis.git
2. Navigate to the project folder:
   ```bash
   cd Palantir_Analysis
3. Install the required libraries:
   ```bash
   pip install -r requirements.txt
4. Run the Palantir interactive dashboard on streamlit:
https://palantirdashboard-ppsfa4dembn7xqmdwx5uhf.streamlit.app/

Additional Analysis
The SWOT analysis and conclusion are embedded in the Streamlit app under the "Additional Analysis" section.

Technologies Used
Python Libraries: yfinance, pandas, numpy, matplotlib, plotly, scikit-learn.

Machine Learning: Linear Regression for stock price prediction.

Visualization: Interactive charts using Plotly and Matplotlib.

License
This project is licensed under the MIT License. See the LICENSE file for details.
