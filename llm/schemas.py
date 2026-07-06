from pydantic import BaseModel

class Intent(BaseModel):
    operation: str
    column: str

