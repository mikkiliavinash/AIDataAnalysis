def validate_file(df):
    if df.empty:
        raise ValueError("File is empty")

    return True