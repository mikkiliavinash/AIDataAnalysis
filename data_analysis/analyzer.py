def execute_operation(df, intent):
    operation = intent.operation.lower()
    column = intent.column

    working_df=df

    filter = intent.filters

    group_by = intent.group_by

    try:
        #Apply Filter        
        
        if filter:
            for f in filter:
                working_df = working_df[working_df[f.column] == f.value]

        if working_df.empty:
            return "No matching records found."

        if filter.column not in df.columns:
                    return f"Column '{filter.column}' doesn't exist."

        #Group BY 
        if group_by:
            if operation == "max":
                result = (working_df.groupby(group_by)[column].max().reset_index())
                print(result)

            elif operation == "min":
                result = (working_df.groupby(group_by)[column].min().reset_index())
                print(result)

            elif operation == "sum":
                result = (working_df.groupby(group_by)[column].sum().reset_index())
                print(result)

            elif operation == "average":
                result = (working_df.groupby(group_by)[column].mean().reset_index())
                print(result)
            elif operation == "count":
                result = (working_df.groupby(group_by).size().reset_index(name="COUNT"))
                print(result)
            else:
                return "Unsupported operation"

            return result
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

        elif operation == "count":
            result = working_df[column].size()
            return result

        else:
            return "Unsupported operation"

    except KeyError as e:
        return f"Error: {e}"