from pydantic import BaseModel, ConfigDict, Field

class TaskIn(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    title: str = Field(min_length=1, max_length=100)
    priority: int = Field(default=3, ge=1, le=5)


class TaskOut(TaskIn):
    model_config = ConfigDict(from_attributes=True)

    id: int
