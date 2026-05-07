from pydantic import BaseModel, Field


class TaskItem(BaseModel):
    id: str
    title: str
    description: str
    priority: str = "medium"
    depends_on: list[str] = Field(default_factory=list)


class TaskList(BaseModel):
    tasks: list[TaskItem] = Field(default_factory=list)
