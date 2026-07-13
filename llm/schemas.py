from pydantic import BaseModel

class Filter(BaseModel):
    column: str
    value: str


class Intent(BaseModel):

    # Aggregation operation
    operation: str | None = None

    # Main column
    column: str | None = None

    # Filters
    filters: list[Filter] | None = None

    # Group By
    group_by: list[str] | None = None

    # Sorting
    sort_by: str | None = None
    sort_order: str | None = None

    # Ranking
    top_n: int | None = None
    bottom_n: int | None = None