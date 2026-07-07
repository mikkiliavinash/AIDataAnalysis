def execute_operation(df, intent):
    operation = intent.operation.lower()
    column = intent.column
    try:
        if operation == "max":
            result = df[column].max()
            return result
        
        if operation == "min":
            result = df[column].min()
            return result
        
        if operation == "sum":
            result = df[column].sum()
            return result

        if operation == "average":
            result = df[column].mean()
            return result

    except Exception as e:
        return f"Error{e}"