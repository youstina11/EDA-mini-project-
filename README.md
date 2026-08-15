# EDA-mini-project-
Building an End-to-End Data Pipeline: Python EDA &amp; SQLite Integration
# Employee Data Analysis & SQLite3 ETL Pipeline

An end-to-end Python pipeline demonstrating Exploratory Data Analysis (EDA), data cleaning, feature engineering, and relational database management using SQLite3.

## Overview
This project processes raw organizational employee records containing missing values, duplicates, and unformatted data types. It cleans and manipulates the data using Pandas/NumPy, loads the structured dataset into a SQLite database, runs analytical SQL queries and database operations, and exports the processed results.

## Key Features
* **Exploratory Data Analysis:** Summary statistics, distribution checks, and missing data profiling.
* **Data Cleaning & Imputation:** Handled missing numeric records via mean/median imputation, eliminated duplicate rows, and cast datatypes (datetime conversion).
* **Feature Engineering:** Calculated dynamic bonus structures, total compensation, and seniority indicators.
* **SQL Pipeline & Management (SQLite3):** 
  * Schema creation, table generation, and data ingestion via `to_sql`.
  * CRUD operations including analytical queries, record insertion, conditional `UPDATE`, and `DELETE`.
  * Aggregation queries for department-level salary benchmarks and top performers.
* **Modular Code & Error Handling:** Packaged ETL workflows into reusable Python functions with `try-except` exception handling.

## Tech Stack
* **Language:** Python
* **Data Manipulation & Analysis:** Pandas, NumPy
* **Database & Querying:** SQLite3, SQL

├── EDA_SQLite_Employee_200.csv     # Raw dataset
├── solution.py                     # Main analysis & SQLite pipeline script
├── employees_final.csv             # Cleaned & transformed export
└── README.md                       # Documentation

## Project Structure
