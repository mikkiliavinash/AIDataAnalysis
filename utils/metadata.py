import pandas as pd

def get_metadata(df):

    rows,column_count =df.shape
    column_names = df.columns.tolist()
    
    
    data_types = df.dtypes.astype(str).reset_index()
    data_types.columns = ["Column", "Data Type"]


    empty_rows = df[df.isnull().all(axis=1)]
    
    num_empty_rows = df.isnull().all(axis=1).sum()

    total_duplicates = df.duplicated().sum()
    duplicate_rows = df[df.duplicated()]

    missing_count= df.isna().sum().sum()

    missing_summary = pd.DataFrame({
    'Missing Cells': df.isna().sum(),
    'Percentage (%)': (df.isna().sum() / len(df)) * 100}).round(2).reset_index()
    missing_summary.columns = ["Column Name","Missing Cells","Percentage (%)"]

    memory_usage = f"{round(df.memory_usage(deep=True).sum() / (1024 * 1024), 2)} MB"

    return {
        "rows":rows,
        "column_count":column_count,
        "column_names":column_names,
        "data_types":data_types,
        "empty_rows":empty_rows,
        "num_empty_rows":num_empty_rows,
        "missing_count":missing_count,
        "missing_summary":missing_summary,
        "total_duplicates":total_duplicates,
        "duplicate_rows":duplicate_rows,
        "memory_usage":memory_usage
    }

