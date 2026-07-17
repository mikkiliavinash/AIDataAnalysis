import pandas as pd

def execute_operation(df, intent):
    operation = intent.operation.lower()
    column = intent.columns

    working_df = df.copy()

    filters = intent.filters
    group_by = intent.group_by

    sort_by = intent.sort_by
    sort_order = intent.sort_order

    top_n = intent.top_n
    bottom_n = intent.bottom_n

    date_filter = intent.date_filter

    try:
            
        if working_df.empty:
            return "No matching records found."
        # -----------------------------
        # Apply Filters
        # -----------------------------
        if filters:
            print("===== IN FILTERS =====")
            for f in filters:
                working_df = working_df[working_df[f.column] == f.value]

            # -----------------------------
            # Apply Date Filter
            # -----------------------------
        if date_filter is not None:
            print("===== IN Date FILTERS =====")
            print("Date Filter:", date_filter)

            working_df[date_filter.column] = pd.to_datetime(working_df[date_filter.column])

            if date_filter.operator == "EQUAL":
                 
                 value = pd.to_datetime(date_filter.value)

                 working_df = working_df[
                      (working_df[date_filter.column].dt.year == value.year) &
                      (working_df[date_filter.column].dt.month == value.month)]

                 print("Rows after filter:", len(working_df))

            elif date_filter.operator == "BEFORE":
                value = pd.to_datetime(date_filter.value)
                working_df = working_df[working_df[date_filter.column] < value]
                print("Rows before:", len(working_df))

            elif date_filter.operator == "AFTER":
                value = pd.to_datetime(date_filter.value)
                working_df = working_df[working_df[date_filter.column] > value]
                print("Rows after:", len(working_df))

            elif date_filter.operator == "BETWEEN":
                start = pd.to_datetime(date_filter.start)
                end = pd.to_datetime(date_filter.end)
                working_df = working_df[
                    (working_df[date_filter.column] >= start) &
                    (working_df[date_filter.column] <= end)
                    ]

        # -----------------------------
        # Group By
        # -----------------------------
        if group_by:
            print("===== IN GROUP BY =====")

            if operation == "sum":
                result = (working_df.groupby(group_by)[column].sum().reset_index())

            elif operation == "average":
                result = (working_df.groupby(group_by)[column].mean().reset_index())

            elif operation == "max":
                result = (working_df.groupby(group_by)[column].max().reset_index())

            elif operation == "min":
                result = (working_df.groupby(group_by)[column].min().reset_index())

            elif operation == "count":
                result = (working_df.groupby(group_by).size().reset_index(name="COUNT"))

            else:
                return "Unsupported operation"

        else:

            # -----------------------------
            # No Group By
            # -----------------------------
           
            

            if operation == "sum":
                results = {}
                for col in column:
                    results[col] = working_df[col].sum()
                    result = pd.DataFrame([results])
                return result
                

            elif operation == "average":
                result = working_df[column].mean()
                return result

            elif operation == "max":
                result = working_df[column].max()
                return result

            elif operation == "min":
                result = working_df[column].min()
                return result

            elif operation == "count":
                result =  working_df[column].count()
                return result

            else:
                return "Unsupported operation"

        # -----------------------------
        # Sorting
        # -----------------------------
        if sort_by:
            print("===== IN SORT BY =====")

            ascending = True

            if sort_order:
                ascending = sort_order.upper() == "ASC"

            result = result.sort_values(
                by=sort_by,
                ascending=ascending
            )

        # -----------------------------
        # Top N
        # -----------------------------
        if top_n:
            result = result.head(top_n)

        # -----------------------------
        # Bottom N
        # -----------------------------
        if bottom_n:
            result = result.tail(bottom_n)

        return result

    except KeyError as e:
        return f"Error: {e}"