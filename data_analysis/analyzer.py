def execute_operation(df, intent):
    operation = intent.operation.lower()
    column = intent.column
    working_df=df
    filter_column = intent.filter_column
    filter_value=intent.filter_value
    try:

        if filter_column:
            working_df=working_df[working_df[filter_column]==filter_value]

        if working_df.empty:
            return "No matching records found."
        
        if operation == "max":
            result = working_df[column].max()
            return result
            
        elif operation == "min":
            result = working_df[column].min()
            return result
            
        elif operation == "sum":
            result = working_df[column].sum()
            return result

        elif operation == "average":
            result = working_df[column].mean()
            return result

        else:
            return "Unsupported operation"

    except KeyError as e:
        return f"Error: {e}"