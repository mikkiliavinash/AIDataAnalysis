from pydantic import BaseModel


class Filter(BaseModel):
    column: str
    value: str

class Intent(BaseModel):
    operation: str
    column: str
    filters: list[Filter] | None = None
    group_by: list[str] | None = None


