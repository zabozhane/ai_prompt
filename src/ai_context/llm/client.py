from typing import TypeVar

from openai import OpenAI
from pydantic import BaseModel

from ai_context.settings import Settings

SchemaT = TypeVar("SchemaT", bound=BaseModel)


class LLMClient:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._client = OpenAI(api_key=settings.openai_api_key)

    def generate_structured(self, *, system: str, user: str, schema: type[SchemaT]) -> SchemaT:
        response = self._client.responses.parse(
            model=self._settings.openai_model,
            input=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            text_format=schema,
        )
        return response.output_parsed
