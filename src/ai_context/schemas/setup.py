from pydantic import BaseModel, Field


class SetupProposal(BaseModel):
    preferred_stack: str
    constraints: list[str] = Field(default_factory=list)
