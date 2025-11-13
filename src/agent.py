"""LangChain-powered LinkedIn post generator using GitHub Models."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Final

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

SUPPORTED_LANGUAGES: Final[dict[str, str]] = {
    "english": "English",
    "bengali": "Bengali",
    "spanish": "Spanish",
}
DEFAULT_BASE_URL: Final[str] = os.environ.get("GITHUB_BASE_URL")
DEFAULT_MODEL_NAME: Final[str] = os.environ.get("GITHUB_MODEL")


@dataclass(slots=True)
class GeneratorConfig:
    """Configuration for the LinkedIn post generator."""

    api_key: str
    base_url: str = DEFAULT_BASE_URL
    model: str = DEFAULT_MODEL_NAME
    temperature: float = 0.7


class LinkedInPostGenerator:
    """Generate LinkedIn-ready posts in the supported languages."""

    def __init__(self, config: GeneratorConfig) -> None:
        self._config = config
        self._llm = ChatOpenAI(
            api_key=config.api_key,
            base_url=config.base_url,
            model=config.model,
            temperature=config.temperature,
        )
        self._prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    (
                        "You are a professional LinkedIn ghostwriter. "
                        "Always write in the requested language, keep a confident yet approachable tone, "
                        "and tailor the post for ambitious professionals. "
                        "When relevant, weave in actionable insights or a concise call-to-action."
                    ),
                ),
                (
                    "human",
                    (
                        "Create a LinkedIn post about '{topic}' in {language}. "
                        "Structure the post into 2 to 4 short paragraphs separated by blank lines. "
                        "Open with a hook, develop the topic with context or a quick story, "
                        "and close with a takeaway or question that drives engagement. "
                        "Avoid using hashtags or emojis."
                    ),
                ),
            ]
        )
        self._chain = self._prompt | self._llm | StrOutputParser()

    def generate_all(self, topic: str) -> dict[str, str]:
        """Generate posts in every supported language."""
        topic_clean = topic.strip()
        outputs: dict[str, str] = {}
        for key, display_name in SUPPORTED_LANGUAGES.items():
            variables = {"topic": topic_clean, "language": display_name}
            outputs[key] = self._chain.invoke(variables).strip()
        return outputs

