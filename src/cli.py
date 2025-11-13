# noqa: D401 - simple CLI module
"""Command line interface for the LinkedIn post generator."""

from __future__ import annotations

import argparse
import os
import sys
from typing import Optional

from dotenv import load_dotenv

from .agent import (
    DEFAULT_BASE_URL,
    DEFAULT_MODEL_NAME,
    SUPPORTED_LANGUAGES,
    GeneratorConfig,
    LinkedInPostGenerator,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate LinkedIn posts with a LangChain-powered GitHub model."
    )
    parser.add_argument(
        "--topic",
        required=True,
        help="Topic or theme of the LinkedIn post.",
    )
    parser.add_argument(
        "--model",
        default=None,
        help="Model name exposed by GitHub Models (default: value from GITHUB_MODEL or openai/gpt-4o).",
    )
    parser.add_argument(
        "--base-url",
        default=None,
        help="Base URL for the GitHub Models inference endpoint (default: value from GITHUB_BASE_URL or https://models.github.ai/inference).",
    )
    return parser


def run(
    *,
    topic: str,
    model: str,
    base_url: str,
    token: Optional[str],
) -> dict[str, str]:
    """Generate LinkedIn posts (English, Bengali, Spanish) for the topic."""
    if not token:
        raise ValueError(
            "Missing GITHUB_TOKEN. Set it in your environment or .env file."
        )
    effective_base_url = base_url or DEFAULT_BASE_URL
    effective_model = model or DEFAULT_MODEL_NAME
    config = GeneratorConfig(
        api_key=token,
        base_url=effective_base_url,
        model=effective_model,
    )
    generator = LinkedInPostGenerator(config)
    return generator.generate_all(topic=topic)


def main(argv: Optional[list[str]] = None) -> int:
    load_dotenv()
    parser = build_parser()
    args = parser.parse_args(argv)
    token = os.getenv("GITHUB_TOKEN")
    base_url = args.base_url or os.getenv("GITHUB_BASE_URL")
    model = args.model or os.getenv("GITHUB_MODEL")
    try:
        posts = run(
            topic=args.topic,
            model=model,
            base_url=base_url,
            token=token,
        )
    except Exception as exc:  # pragma: no cover - user-facing error path.
        parser.error(str(exc))
        return 2
    for lang_code, display_name in SUPPORTED_LANGUAGES.items():
        post = posts.get(lang_code)
        if not post:
            continue
        heading = f"{display_name} ({lang_code})"
        underline = "-" * len(heading)
        print(f"\n{heading}\n{underline}\n{post.strip()}\n")
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())

