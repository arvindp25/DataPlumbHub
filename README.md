# DataPlumbHub
1. Project Overview

Objective

The goal of this project is to build an investment portfolio analysis system using the bigquery-public-data.cymbal_investments dataset. The system will leverage Google Cloud Dataproc (PySpark) to process financial data, assess portfolio performance, calculate risk metrics, and generate insights through reports.

2. Key Features & Scope

2.1 Features

Data Ingestion: Extract investment transaction data from BigQuery.

Portfolio Performance Analysis: Compute return, risk, and diversification.

Risk Metrics Calculation: Measure Sharpe Ratio, Standard Deviation, Beta.

Asset Allocation Insights: Analyze sector diversification & top-performing investments.

Report Generation: Provide visual insights using Looker Studio.

Predictive Analytics (Optional): Use BigQuery ML to forecast returns.

2.2 Out of Scope

Real-time portfolio tracking (can be a future extension with Dataflow & Pub/Sub).

Integration with live stock market data.

3. Data & Schema

3.1 Source Data (BigQuery - bigquery-public-data.cymbal_investments.transactions)

Key columns from transactions table:

transaction_id: Unique ID for the transaction.

customer_id: Unique investor ID.

amount: Transaction amount (USD).

transaction_type: Buy/Sell.

investment_type: Stock, Bond, ETF, etc.

timestamp: Date & time of transaction.

symbol: Ticker symbol of investment.

units: Number of units purchased or sold.

price_per_unit: Price per unit of the investment.

3.2 Processed Data (Portfolio Metrics Output in BigQuery)

customer_id

total_investment: Total amount invested.

portfolio_return: Portfolio return %.

portfolio_risk: Standard deviation of returns.

sharpe_ratio: Return per unit of risk.

top_assets: Top 3 performing assets per investor.

diversification_score: Portfolio sector diversification index.

4. System Architecture

4.1 Tech Stack

Data Source: Google BigQuery (Public Dataset)

Processing Engine: PySpark on Google Cloud Dataproc

Storage: Google Cloud Storage (for intermediate processing)

ML Model: BigQuery ML (for return prediction)

Reporting: Looker Studio / Tableau

Orchestration: Apache Airflow or Cloud Composer (for scheduling batch jobs)

4.2 Data Pipeline

Extract Data: Query transaction data from BigQuery.

Transform Data: Aggregate investments per customer, compute returns.

Compute Portfolio Metrics: Risk, Sharpe Ratio, Sector Allocation.

Store Processed Data: Write aggregated insights to BigQuery.

Generate Reports: Provide summary dashboards using Looker Studio.

5. Reporting & Dashboards

5.1 Reports

Portfolio Summary Report: Total investment, return, and risk per customer.

Top Asset Allocation Report: Most profitable investments per sector.

Customer Investment Trends: Historical investment patterns.

Risk vs. Return Analysis: Plot risk vs. returns for different investors.

6. Performance Metrics

Portfolio Performance Accuracy: Comparison with benchmark indices.

Processing Time: Execution speed of Dataproc pipeline.

Scalability: Ability to process large datasets efficiently.

7. Next Steps

Set up Google Cloud Dataproc Cluster.

Query & explore bigquery-public-data.cymbal_investments.transactions.

Implement PySpark ETL pipeline.

Compute portfolio performance metrics.

Build reports in Looker Studio.