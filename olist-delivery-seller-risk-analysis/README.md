# Olist Delivery Performance & Seller Risk Analysis

Analysis of the Brazilian e-commerce Olist dataset, examining delivery performance and building a seller-level risk scoring model.

## Key Findings
- Overall on-time delivery rate: 90.7% across 113,425 orders
- Regional gap: South/Southeast regions outperform Northeast on both on-time rate and review scores
- Late delivery strongly predicts poor reviews: average score drops from 4.11 (on time) to 1.70 (very late)
- Built a seller risk-scoring model identifying 81 high-risk sellers (4.3%) out of 1,894 sellers with reliable order history

## Contents
- `01_data_cleaning.ipynb` — merging and cleaning raw order, item, seller, and review data
- `02_exploratory_analysis.ipynb` — on-time rate, regional analysis, delay-vs-review relationship
- `03_seller_risk_analysis.ipynb` — seller-level risk scoring and tiering
- `data_processed/` — cleaned datasets and risk score outputs

## Data Source
[Olist Brazilian E-Commerce Public Dataset on Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

## Tools
Python, pandas, Jupyter Notebook
