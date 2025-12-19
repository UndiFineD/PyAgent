# Data Lakehouses

## Overview
A **Data Lakehouse** is a modern data architecture that combines the flexibility and low cost of a **Data Lake** with the data management and ACID transaction features of a **Data Warehouse**. It is the foundation for scalable AI and ML workloads.

## Evolution
1.  **Data Warehouse (1990s)**: Structured data (SQL), expensive, schema-on-write. Good for BI/Reporting.
2.  **Data Lake (2010s)**: Unstructured data (Hadoop/S3), cheap, schema-on-read. Good for ML but prone to becoming a "Data Swamp" (messy, unreliable).
3.  **Data Lakehouse (2020s)**: Best of both. Stores data in open formats (Parquet) on cheap storage (S3) but adds a transaction layer for reliability.

## Key Technologies (Table Formats)
The "magic" of a Lakehouse lies in the open table formats that provide metadata management:

### 1. Delta Lake (Databricks)
*   **ACID Transactions**: Ensures that data is either fully written or not at all (no partial files).
*   **Time Travel**: Query data as it existed at a specific point in time (useful for reproducing ML experiments).
*   **Schema Enforcement**: Prevents bad data from corrupting tables.

### 2. Apache Iceberg (Netflix)
*   **Hidden Partitioning**: Handles partitioning automatically (e.g., querying by "Month" even if data is partitioned by "Day").
*   **Schema Evolution**: Supports adding/renaming columns without rewriting the entire dataset.

### 3. Apache Hudi (Uber)
*   **Upserts**: Optimized for streaming data and frequent updates (Insert + Update).
*   **Incremental Processing**: Allows processing only the new data that arrived since the last run.

## Benefits for AI
*   **Single Source of Truth**: No need to copy data from a Warehouse to a Lake for training.
*   **Support for All Data**: Handles text, images, and video alongside structured customer tables.
*   **Performance**: Query engines (Spark, Trino) are highly optimized for these formats.
