from pydantic import BaseModel

class Intent(BaseModel):
    operation: str
    column: str
    filter_column : str | None=None
    filter_value : str| None=None
