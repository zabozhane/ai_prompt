from pydantic import BaseModel, Field


class ProjectSpec(BaseModel):
    project_name: str
    idea: str
    preferred_stack: str
    constraints: list[str] = Field(default_factory=list)
    goals: list[str] = Field(default_factory=list)
    non_goals: list[str] = Field(default_factory=list)
