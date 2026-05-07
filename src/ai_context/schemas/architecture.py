from pydantic import BaseModel, Field


class ComponentSpec(BaseModel):
    name: str
    purpose: str
    responsibilities: list[str] = Field(default_factory=list)


class ArchitectureSpec(BaseModel):
    overview: str
    components: list[ComponentSpec] = Field(default_factory=list)
    data_flow: list[str] = Field(default_factory=list)
