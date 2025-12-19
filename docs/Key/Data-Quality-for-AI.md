# Data Quality for AI

## Overview
**Data Quality** is the practice of validating data before it enters an AI model. "Garbage In, Garbage Out" is the golden rule of ML. If the training data is corrupt, biased, or missing, the model will fail regardless of the architecture.

## Dimensions of Data Quality
1.  **Completeness**: Are there missing values (Nulls)?
2.  **Uniqueness**: Are there duplicate rows?
3.  **Timeliness**: Is the data fresh?
4.  **Validity**: Does the data conform to the schema (e.g., Age > 0, Email contains "@")?
5.  **Consistency**: Is the data the same across different tables?

## Testing Frameworks

### 1. Great Expectations (GX)
The most popular open-source library for data validation.
*   **Expectations**: Assertions about data (e.g., `expect_column_values_to_be_between(min=0, max=100)`).
*   **Data Docs**: Automatically generates HTML documentation showing which tests passed/failed.
*   **Integration**: Works with Pandas, Spark, and SQL databases.

### 2. Pandera
A lightweight validation library for Pandas DataFrames.
*   **Schema Models**: Define schemas using Python classes (Pydantic-style).
*   **Runtime Checks**: Validates data as it flows through the pipeline functions.

### 3. Soda Core
A SQL-native data quality tool.
*   **SodaCL**: A YAML-based language for defining checks (`row_count > 0`).

## Data Drift vs. Data Quality
*   **Data Quality**: Checks for *errors* (Nulls, invalid types). "Is the data broken?"
*   **Data Drift**: Checks for *statistical changes* (Distribution shift). "Has the world changed?" (Covered in [MLOps.md](MLOps.md)).

## Best Practices
*   **Circuit Breakers**: If data quality drops below a threshold (e.g., >5% nulls), stop the pipeline immediately to prevent training a bad model.
*   **Shift-Left**: Validate data as early as possible (at ingestion), not just before training.
