def format_metadata(metadata):

    output = []

    data_types = metadata["data_types"]

    for _, row in data_types.iterrows():

        column = row.iloc[0]      # First column
        dtype = str(row.iloc[1]).lower()   # Second column

        if "int" in dtype or "float" in dtype:
            column_type = "numeric"

        elif "datetime" in dtype:
            column_type = "datetime"

        elif "bool" in dtype:
            column_type = "boolean"

        elif "object" in dtype or "string" in dtype:
            column_type = "text/categorical"

        else:
            column_type = dtype

        output.append(f"- {column} ({column_type})")

    return "\n".join(output)