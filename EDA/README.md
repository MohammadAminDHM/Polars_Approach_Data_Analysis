# Exploratory Data Analysis (EDA) with Polars

## Introduction

Polars is a blazingly fast DataFrame library implemented in Rust with bindings for Python. It's designed for high performance data manipulation and analysis, making it an excellent choice for EDA tasks.

## Installation

```bash
pip install polars
```

## Basic Operations

### 1. Importing Data

```python
import polars as pl

# Read CSV
df = pl.read_csv("data.csv")

# Read Parquet
df = pl.read_parquet("data.parquet")

# Read Excel
df = pl.read_excel("data.xlsx")
```

### 2. Basic DataFrame Operations

```python
# View first few rows
df.head()

# Get DataFrame shape
df.shape

# Get column names
df.columns

# Get data types
df.dtypes

# Get summary statistics
df.describe()
```

## Common EDA Techniques

### 1. Data Overview

```python
# Check for missing values
df.null_count()

# Get unique values in a column
df["column_name"].unique()

# Get value counts
df["column_name"].value_counts()
```

### 2. Statistical Analysis

```python
# Basic statistics
df.select([
    pl.col("numeric_column").mean(),
    pl.col("numeric_column").median(),
    pl.col("numeric_column").std(),
    pl.col("numeric_column").min(),
    pl.col("numeric_column").max()
])

# Correlation matrix
df.select(pl.corr("column1", "column2"))
```

### 3. Data Visualization

While Polars doesn't have built-in visualization capabilities, it works well with libraries like Matplotlib and Seaborn:

```python
import matplotlib.pyplot as plt
import seaborn as sns

# Convert to pandas for visualization
df_pd = df.to_pandas()

# Create a histogram
plt.figure(figsize=(10, 6))
sns.histplot(data=df_pd, x="column_name")
plt.show()
```

### 4. Data Cleaning

```python
# Drop missing values
df.drop_nulls()

# Fill missing values
df.fill_null(0)  # Fill with 0
df.fill_null(strategy="forward")  # Forward fill

# Remove duplicates
df.unique()
```

### 5. Grouping and Aggregation

```python
# Group by and aggregate
df.groupby("category_column").agg([
    pl.col("numeric_column").mean(),
    pl.col("numeric_column").count(),
    pl.col("numeric_column").sum()
])
```

## Advanced EDA Techniques

### 1. Time Series Analysis

```python
# Convert to datetime
df = df.with_columns(
    pl.col("date_column").str.strptime(pl.Date, "%Y-%m-%d")
)

# Resample time series data
df.groupby_dynamic("date_column", every="1d").agg([
    pl.col("value").mean()
])
```

### 2. Feature Engineering

```python
# Create new features
df = df.with_columns([
    (pl.col("column1") + pl.col("column2")).alias("new_feature"),
    (pl.col("column1") * pl.col("column2")).alias("interaction")
])
```

### 3. Data Quality Checks

```python
# Check for outliers using IQR
q1 = df["numeric_column"].quantile(0.25)
q3 = df["numeric_column"].quantile(0.75)
iqr = q3 - q1
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr

outliers = df.filter(
    (pl.col("numeric_column") < lower_bound) |
    (pl.col("numeric_column") > upper_bound)
)
```

## Best Practices

1. **Memory Efficiency**: Polars is memory efficient by default, but you can further optimize by:
   - Using appropriate data types
   - Processing data in chunks when dealing with large datasets
   - Using lazy evaluation when possible

2. **Performance Tips**:
   - Use vectorized operations instead of loops
   - Leverage Polars' parallel processing capabilities
   - Use appropriate data types for columns

3. **Code Organization**:
   - Keep your EDA code modular and well-documented
   - Save intermediate results when working with large datasets
   - Use functions to encapsulate common EDA operations

## Example EDA Workflow

```python
def perform_eda(df):
    # 1. Initial data overview
    print("Data Overview:")
    print(df.head())
    print("\nShape:", df.shape)
    print("\nColumns:", df.columns)
    
    # 2. Check for missing values
    print("\nMissing Values:")
    print(df.null_count())
    
    # 3. Basic statistics
    print("\nBasic Statistics:")
    print(df.describe())
    
    # 4. Data quality checks
    print("\nData Quality Checks:")
    for col in df.columns:
        if df[col].dtype in [pl.Float64, pl.Int64]:
            print(f"\n{col} statistics:")
            print(df[col].describe())
```

## Resources

- [Polars Documentation](https://pola-rs.github.io/polars/py-polars/html/reference/index.html)
- [Polars User Guide](https://pola-rs.github.io/polars-book/user-guide/index.html)
- [Polars GitHub Repository](https://github.com/pola-rs/polars)

## Next Steps

1. Practice with real-world datasets
2. Explore more advanced Polars features
3. Learn about performance optimization
4. Integrate Polars with other data science tools
