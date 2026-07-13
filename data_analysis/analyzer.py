def execute_operation(df, intent):

    operation = intent.operation.lower()
    column = intent.column

    working_df = df.copy()

    filters = intent.filters
    group_by = intent.group_by

    sort_by = intent.sort_by
    sort_order = intent.sort_order

    top_n = intent.top_n
    bottom_n = intent.bottom_n

    try:

        # -----------------------------
        # Apply Filters
        # -----------------------------
        if filters:
            for f in filters:
                working_df = working_df[
                    working_df[f.column] == f.value
                ]

        if working_df.empty:
            return "No matching records found."

        # -----------------------------
        # Group By
        # -----------------------------
        if group_by:

            if operation == "sum":
                result = (working_df.groupby(group_by)[column].sum().reset_index())
                temp = working_df.groupby(group_by)[column].sum()
                print(type(temp))
                print(type(temp.reset_index))

            elif operation == "average":
                result = (
                    working_df
                    .groupby(group_by)[column]
                    .mean()
                    .reset_index()
                )

            elif operation == "max":
                result = (
                    working_df
                    .groupby(group_by)[column]
                    .max()
                    .reset_index()
                )

            elif operation == "min":
                result = (
                    working_df
                    .groupby(group_by)[column]
                    .min()
                    .reset_index()
                )

            elif operation == "count":
                result = (
                    working_df
                    .groupby(group_by)
                    .size()
                    .reset_index(name="COUNT")
                )

            else:
                return "Unsupported operation"

        else:

            # -----------------------------
            # No Group By
            # -----------------------------
            if operation == "sum":
                return working_df[column].sum()

            elif operation == "average":
                return working_df[column].mean()

            elif operation == "max":
                return working_df[column].max()

            elif operation == "min":
                return working_df[column].min()

            elif operation == "count":
                return working_df[column].count()

            else:
                return "Unsupported operation"

        # -----------------------------
        # Sorting
        # -----------------------------
        if sort_by:

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