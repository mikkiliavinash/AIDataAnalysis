import pandas as pd
from pandas.api.types import is_datetime64_any_dtype

def select_chart(result):

    if not isinstance(result, pd.DataFrame):
        return None

    if result.empty:
        return None

    # Single row = KPI/cards, not charts
    if len(result) == 1:
        return None

    if len(result.columns) != 2:
        return None

    first_col = result.columns[0]

    if is_datetime64_any_dtype(result[first_col]):
        return "line"

    if result[first_col].nunique() <= 8:
        return "pie"

    return "bar"