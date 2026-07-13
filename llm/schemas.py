from pydantic import BaseModel

class DateFilter(BaseModel):
    column: str

    operator: str
    # EQUAL, BEFORE, AFTER, BETWEEN

    value: str | None = None

    start: str | None = None

    end: str | None = None

class Filter(BaseModel):
    column: str
    value: str


class Intent(BaseModel):

    operation: str | None = None

    column: str | None = None

    filters: list[Filter] | None = None

    date_filter: DateFilter | None = None

    group_by: list[str] | None = None

    sort_by: str | None = None

    sort_order: str | None = None

    top_n: int | None = None

    bottom_n: int | None = None