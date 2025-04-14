"""
Polars EDA Module

This module provides functions for performing Exploratory Data Analysis (EDA) using Polars.
It includes functions for data overview, statistical analysis, visualization, and data quality checks.
"""

import polars as pl
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Union, List, Optional
import numpy as np


def get_data_overview(df: pl.DataFrame) -> None:
    """
    Display basic information about the DataFrame.
    
    Args:
        df (pl.DataFrame): Input DataFrame
    """
    print("Data Overview:")
    print(df.head())
    print("\nShape:", df.shape)
    print("\nColumns:", df.columns)
    print("\nData types:", df.dtypes)
    print("\nMissing values:")
    print(df.null_count())


def get_numeric_statistics(df: pl.DataFrame, columns: Optional[List[str]] = None) -> pl.DataFrame:
    """
    Calculate basic statistics for numeric columns.
    
    Args:
        df (pl.DataFrame): Input DataFrame
        columns (List[str], optional): List of columns to analyze. If None, all numeric columns are used.
    
    Returns:
        pl.DataFrame: DataFrame containing statistics
    """
    if columns is None:
        numeric_cols = [col for col, dtype in zip(df.columns, df.dtypes) 
                       if dtype in [pl.Float64, pl.Int64]]
    else:
        numeric_cols = columns
    
    stats = df.select([
        pl.col(col).mean().alias(f'mean_{col}'),
        pl.col(col).median().alias(f'median_{col}'),
        pl.col(col).std().alias(f'std_{col}'),
        pl.col(col).min().alias(f'min_{col}'),
        pl.col(col).max().alias(f'max_{col}')
        for col in numeric_cols
    ])
    
    return stats


def get_categorical_statistics(df: pl.DataFrame, columns: Optional[List[str]] = None) -> dict:
    """
    Calculate statistics for categorical columns.
    
    Args:
        df (pl.DataFrame): Input DataFrame
        columns (List[str], optional): List of columns to analyze. If None, all categorical columns are used.
    
    Returns:
        dict: Dictionary containing value counts for each categorical column
    """
    if columns is None:
        categorical_cols = [col for col, dtype in zip(df.columns, df.dtypes) 
                          if dtype == pl.Utf8]
    else:
        categorical_cols = columns
    
    stats = {}
    for col in categorical_cols:
        stats[col] = df[col].value_counts()
    
    return stats


def plot_distributions(df: pl.DataFrame, 
                      numeric_cols: Optional[List[str]] = None,
                      categorical_cols: Optional[List[str]] = None,
                      figsize: tuple = (15, 10)) -> None:
    """
    Create distribution plots for numeric and categorical columns.
    
    Args:
        df (pl.DataFrame): Input DataFrame
        numeric_cols (List[str], optional): List of numeric columns to plot
        categorical_cols (List[str], optional): List of categorical columns to plot
        figsize (tuple): Figure size
    """
    df_pd = df.to_pandas()
    sns.set_style('whitegrid')
    
    if numeric_cols is None:
        numeric_cols = [col for col, dtype in zip(df.columns, df.dtypes) 
                       if dtype in [pl.Float64, pl.Int64]]
    
    if categorical_cols is None:
        categorical_cols = [col for col, dtype in zip(df.columns, df.dtypes) 
                          if dtype == pl.Utf8]
    
    # Calculate number of plots needed
    n_plots = len(numeric_cols) + len(categorical_cols)
    n_rows = (n_plots + 1) // 2
    
    fig, axes = plt.subplots(n_rows, 2, figsize=figsize)
    axes = axes.flatten()
    
    # Plot numeric distributions
    for i, col in enumerate(numeric_cols):
        sns.histplot(data=df_pd, x=col, ax=axes[i])
        axes[i].set_title(f'{col} Distribution')
    
    # Plot categorical distributions
    for i, col in enumerate(categorical_cols, len(numeric_cols)):
        sns.countplot(data=df_pd, x=col, ax=axes[i])
        axes[i].set_title(f'{col} Distribution')
        axes[i].tick_params(axis='x', rotation=45)
    
    # Hide empty subplots
    for i in range(n_plots, len(axes)):
        axes[i].set_visible(False)
    
    plt.tight_layout()
    plt.show()


def detect_outliers(df: pl.DataFrame, 
                   columns: Optional[List[str]] = None,
                   threshold: float = 1.5) -> dict:
    """
    Detect outliers using the Interquartile Range (IQR) method.
    
    Args:
        df (pl.DataFrame): Input DataFrame
        columns (List[str], optional): List of columns to analyze. If None, all numeric columns are used.
        threshold (float): Threshold for outlier detection (default: 1.5)
    
    Returns:
        dict: Dictionary containing outlier information for each column
    """
    if columns is None:
        columns = [col for col, dtype in zip(df.columns, df.dtypes) 
                  if dtype in [pl.Float64, pl.Int64]]
    
    outliers = {}
    for col in columns:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - threshold * iqr
        upper_bound = q3 + threshold * iqr
        
        outlier_mask = (df[col] < lower_bound) | (df[col] > upper_bound)
        outlier_count = df.filter(outlier_mask).height
        
        outliers[col] = {
            'count': outlier_count,
            'percentage': (outlier_count / df.height) * 100,
            'lower_bound': lower_bound,
            'upper_bound': upper_bound
        }
    
    return outliers


def analyze_correlations(df: pl.DataFrame, 
                        columns: Optional[List[str]] = None) -> pl.DataFrame:
    """
    Calculate correlation matrix for numeric columns.
    
    Args:
        df (pl.DataFrame): Input DataFrame
        columns (List[str], optional): List of columns to analyze. If None, all numeric columns are used.
    
    Returns:
        pl.DataFrame: Correlation matrix
    """
    if columns is None:
        columns = [col for col, dtype in zip(df.columns, df.dtypes) 
                  if dtype in [pl.Float64, pl.Int64]]
    
    # Create correlation matrix
    corr_matrix = pl.DataFrame()
    for i, col1 in enumerate(columns):
        correlations = []
        for col2 in columns:
            if col1 == col2:
                correlations.append(1.0)
            else:
                correlations.append(df.select(pl.corr(col1, col2)).item())
        corr_matrix = corr_matrix.with_columns(pl.Series(col1, correlations))
    
    return corr_matrix


def perform_time_series_analysis(df: pl.DataFrame,
                               date_column: str,
                               value_column: str,
                               freq: str = '1mo') -> pl.DataFrame:
    """
    Perform time series analysis on the data.
    
    Args:
        df (pl.DataFrame): Input DataFrame
        date_column (str): Name of the date column
        value_column (str): Name of the value column to analyze
        freq (str): Frequency for grouping (default: '1mo')
    
    Returns:
        pl.DataFrame: Time series statistics
    """
    return df.groupby_dynamic(
        date_column,
        every=freq
    ).agg([
        pl.col(value_column).mean().alias(f'mean_{value_column}'),
        pl.col(value_column).median().alias(f'median_{value_column}'),
        pl.col(value_column).std().alias(f'std_{value_column}'),
        pl.count().alias('count')
    ])


def create_features(df: pl.DataFrame,
                   numeric_pairs: Optional[List[tuple]] = None,
                   log_columns: Optional[List[str]] = None) -> pl.DataFrame:
    """
    Create new features from existing columns.
    
    Args:
        df (pl.DataFrame): Input DataFrame
        numeric_pairs (List[tuple], optional): List of column pairs to create ratio features
        log_columns (List[str], optional): List of columns to create log transformations
    
    Returns:
        pl.DataFrame: DataFrame with new features
    """
    new_features = []
    
    # Create ratio features
    if numeric_pairs:
        for col1, col2 in numeric_pairs:
            new_features.append(
                (pl.col(col1) / pl.col(col2)).alias(f'{col1}_per_{col2}')
            )
    
    # Create log transformations
    if log_columns:
        for col in log_columns:
            new_features.append(
                pl.col(col).log().alias(f'log_{col}')
            )
    
    return df.with_columns(new_features)


def perform_complete_eda(df: pl.DataFrame,
                        numeric_cols: Optional[List[str]] = None,
                        categorical_cols: Optional[List[str]] = None,
                        date_column: Optional[str] = None,
                        value_column: Optional[str] = None) -> None:
    """
    Perform a complete EDA workflow.
    
    Args:
        df (pl.DataFrame): Input DataFrame
        numeric_cols (List[str], optional): List of numeric columns to analyze
        categorical_cols (List[str], optional): List of categorical columns to analyze
        date_column (str, optional): Name of the date column for time series analysis
        value_column (str, optional): Name of the value column for time series analysis
    """
    print("=== Data Overview ===")
    get_data_overview(df)
    
    print("\n=== Numeric Statistics ===")
    numeric_stats = get_numeric_statistics(df, numeric_cols)
    print(numeric_stats)
    
    print("\n=== Categorical Statistics ===")
    categorical_stats = get_categorical_statistics(df, categorical_cols)
    for col, stats in categorical_stats.items():
        print(f"\n{col} value counts:")
        print(stats)
    
    print("\n=== Outlier Analysis ===")
    outliers = detect_outliers(df, numeric_cols)
    for col, info in outliers.items():
        print(f"\n{col}:")
        print(f"Number of outliers: {info['count']}")
        print(f"Percentage: {info['percentage']:.2f}%")
        print(f"Lower bound: {info['lower_bound']:.2f}")
        print(f"Upper bound: {info['upper_bound']:.2f}")
    
    print("\n=== Correlation Analysis ===")
    correlations = analyze_correlations(df, numeric_cols)
    print(correlations)
    
    if date_column and value_column:
        print("\n=== Time Series Analysis ===")
        time_series = perform_time_series_analysis(df, date_column, value_column)
        print(time_series)
    
    print("\n=== Distribution Plots ===")
    plot_distributions(df, numeric_cols, categorical_cols) 