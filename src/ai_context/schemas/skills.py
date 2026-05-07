from pydantic import BaseModel, Field


class SkillPack(BaseModel):
    id: str
    title: str
    summary: str
    prompts: list[str] = Field(default_factory=list)
    rules: list[str] = Field(default_factory=list)
    conventions: list[str] = Field(default_factory=list)
    architecture_guidance: list[str] = Field(default_factory=list)
    pitfalls: list[str] = Field(default_factory=list)
    source_files: list[str] = Field(default_factory=list)
    source: str = "local_pack"
    confidence: str = "high"
    match_reason: str = ""


class GeneratedSkillDraft(BaseModel):
    title: str
    summary: str
    rules: list[str] = Field(default_factory=list)
    conventions: list[str] = Field(default_factory=list)
    architecture_guidance: list[str] = Field(default_factory=list)
    pitfalls: list[str] = Field(default_factory=list)
    prompts: list[str] = Field(default_factory=list)


class SkillsFallbackProposal(BaseModel):
    generated_skills: list[GeneratedSkillDraft] = Field(default_factory=list)
    selection_rationale: list[str] = Field(default_factory=list)
    mcp_recommendations: list[str] = Field(default_factory=list)


class SkillsContext(BaseModel):
    selected_skills: list[SkillPack] = Field(default_factory=list)
    selection_rationale: list[str] = Field(default_factory=list)
    mcp_recommendations: list[str] = Field(default_factory=list)
