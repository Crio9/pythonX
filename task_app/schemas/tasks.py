from pydantic import BaseModel, Field

class TaskIn(BaseModel):
    title: str
    priority: int = Field(default=10, ge=1, le=5)