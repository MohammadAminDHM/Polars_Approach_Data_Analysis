# Polars EDA Module Documentation

## Overview

The Polars EDA module provides a comprehensive set of tools for performing Exploratory Data Analysis (EDA) using Polars, a high-performance DataFrame library. This documentation will guide you through the installation, basic usage, and advanced features of the module.

## Installation

```bash
pip install polars matplotlib seaborn
```

## Basic Usage

### Importing the Module

```python
import polars as pl
from polars_eda import perform_complete_eda
```

### Quick Start

Here's a simple example of how to use the module with a sample dataset:

```python
# Create a sample DataFrame
df = pl.DataFrame({
    'age': [25, 30, 35, 40, 45],
    'income': [50000, 60000, 70000, 80000, 90000],
    'education': ['High School', 'Bachelor', 'Master', 'PhD', 'Bachelor']
})

# Perform complete EDA
perform_complete_eda(
    df,
    numeric_cols=['age', 'income'],
    categorical_cols=['education']
)
```

## Function Reference

### 1. Data Overview

#### `get_data_overview(df)`
Displays basic information about the DataFrame.

```python
from polars_eda import get_data_overview

get_data_overview(df)
```

### 2. Statistical Analysis

#### `get_numeric_statistics(df, columns=None)`
Calculates basic statistics for numeric columns.

```python
from polars_eda import get_numeric_statistics

# Get statistics for all numeric columns
stats = get_numeric_statistics(df)

# Get statistics for specific columns
stats = get_numeric_statistics(df, columns=['age', 'income'])
```

#### `get_categorical_statistics(df, columns=None)`
Calculates statistics for categorical columns.

```python
from polars_eda import get_categorical_statistics

# Get statistics for all categorical columns
stats = get_categorical_statistics(df)

# Get statistics for specific columns
stats = get_categorical_statistics(df, columns=['education'])
```

### 3. Visualization

#### `plot_distributions(df, numeric_cols=None, categorical_cols=None, figsize=(15, 10))`
Creates distribution plots for numeric and categorical columns.

```python
from polars_eda import plot_distributions

# Plot all distributions
plot_distributions(df)

# Plot specific columns
plot_distributions(
    df,
    numeric_cols=['age', 'income'],
    categorical_cols=['education']
)
```

### 4. Data Quality

#### `detect_outliers(df, columns=None, threshold=1.5)`
Detects outliers using the IQR method.

```python
from polars_eda import detect_outliers

# Detect outliers in all numeric columns
outliers = detect_outliers(df)

# Detect outliers in specific columns
outliers = detect_outliers(df, columns=['income'])

# Custom threshold
outliers = detect_outliers(df, threshold=2.0)
```

#### `analyze_correlations(df, columns=None)`
Calculates correlation matrix for numeric columns.

```python
from polars_eda import analyze_correlations

# Analyze correlations for all numeric columns
correlations = analyze_correlations(df)

# Analyze correlations for specific columns
correlations = analyze_correlations(df, columns=['age', 'income'])
```

### 5. Time Series Analysis

#### `perform_time_series_analysis(df, date_column, value_column, freq='1mo')`
Performs time series analysis on the data.

```python
from polars_eda import perform_time_series_analysis

# Monthly analysis
monthly_stats = perform_time_series_analysis(
    df,
    date_column='date',
    value_column='value'
)

# Weekly analysis
weekly_stats = perform_time_series_analysis(
    df,
    date_column='date',
    value_column='value',
    freq='1w'
)
```

### 6. Feature Engineering

#### `create_features(df, numeric_pairs=None, log_columns=None)`
Creates new features from existing columns.

```python
from polars_eda import create_features

# Create ratio features
df_enhanced = create_features(
    df,
    numeric_pairs=[('income', 'age')]
)

# Create log transformations
df_enhanced = create_features(
    df,
    log_columns=['income']
)

# Both ratio and log features
df_enhanced = create_features(
    df,
    numeric_pairs=[('income', 'age')],
    log_columns=['income']
)
```

### 7. Complete EDA Workflow

#### `perform_complete_eda(df, numeric_cols=None, categorical_cols=None, date_column=None, value_column=None)`
Performs a complete EDA workflow.

```python
from polars_eda import perform_complete_eda

# Basic EDA
perform_complete_eda(
    df,
    numeric_cols=['age', 'income'],
    categorical_cols=['education']
)

# EDA with time series
perform_complete_eda(
    df,
    numeric_cols=['age', 'income'],
    categorical_cols=['education'],
    date_column='date',
    value_column='value'
)
```

## Advanced Usage

### Customizing Visualizations

The `plot_distributions` function can be customized with different parameters:

```python
# Custom figure size
plot_distributions(df, figsize=(20, 15))

# Custom columns and style
plot_distributions(
    df,
    numeric_cols=['age', 'income'],
    categorical_cols=['education'],
    figsize=(12, 8)
)
```

### Handling Large Datasets

For large datasets, you can use Polars' lazy evaluation:

```python
# Create a lazy DataFrame
lazy_df = pl.scan_csv('large_dataset.csv')

# Perform EDA on a sample
sample_df = lazy_df.limit(10000).collect()
perform_complete_eda(sample_df)
```

### Saving Results

You can save the results of your analysis:

```python
# Save statistics to CSV
stats = get_numeric_statistics(df)
stats.write_csv('numeric_statistics.csv')

# Save correlation matrix
correlations = analyze_correlations(df)
correlations.write_csv('correlations.csv')
```

## Best Practices

1. **Data Preparation**:
   - Ensure your data is properly loaded and cleaned before analysis
   - Handle missing values appropriately
   - Convert data types as needed

2. **Performance**:
   - Use lazy evaluation for large datasets
   - Process data in chunks when necessary
   - Use appropriate data types for better performance

3. **Visualization**:
   - Choose appropriate plot types for your data
   - Customize plots for better readability
   - Save important visualizations

4. **Documentation**:
   - Document your analysis process
   - Save intermediate results
   - Keep track of important findings

## Troubleshooting

### Common Issues

1. **Memory Errors**:
   - Use lazy evaluation
   - Process data in chunks
   - Reduce data size if possible

2. **Visualization Issues**:
   - Check data types
   - Handle missing values
   - Adjust figure size

3. **Performance Issues**:
   - Use appropriate data types
   - Optimize queries
   - Use lazy evaluation

### Getting Help

If you encounter issues:
1. Check the Polars documentation
2. Review the function docstrings
3. Search for similar issues in the Polars community

## Examples

### Example 1: Basic EDA

```python
import polars as pl
from polars_eda import perform_complete_eda

# Load data
df = pl.read_csv('data.csv')

# Perform EDA
perform_complete_eda(
    df,
    numeric_cols=['age', 'income'],
    categorical_cols=['education', 'gender']
)
```

### Example 2: Time Series Analysis

```python
import polars as pl
from polars_eda import perform_time_series_analysis

# Load time series data
df = pl.read_csv('time_series.csv')

# Analyze monthly trends
monthly_stats = perform_time_series_analysis(
    df,
    date_column='date',
    value_column='value',
    freq='1mo'
)
```

### Example 3: Feature Engineering

```python
import polars as pl
from polars_eda import create_features

# Load data
df = pl.read_csv('data.csv')

# Create new features
df_enhanced = create_features(
    df,
    numeric_pairs=[('income', 'age'), ('income', 'experience')],
    log_columns=['income']
)
```

## Contributing

Feel free to contribute to this module by:
1. Reporting issues
2. Suggesting improvements
3. Adding new features
4. Improving documentation

## License

This module is open-source and available under the MIT License. 