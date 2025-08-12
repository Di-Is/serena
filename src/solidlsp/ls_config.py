"""
Configuration objects for language servers
"""

import fnmatch
from collections.abc import Iterable
from dataclasses import dataclass, field
from enum import Enum
from typing import Self


class FilenameMatcher:
    def __init__(self, *patterns: str) -> None:
        """
        :param patterns: fnmatch-compatible patterns
        """
        self.patterns = patterns

    def is_relevant_filename(self, fn: str) -> bool:
        for pattern in self.patterns:
            if fnmatch.fnmatch(fn, pattern):
                return True
        return False


class Language(str, Enum):
    """
    Possible languages with Multilspy.
    """

    MARKDOWN = "markdown"

    @classmethod
    def iter_all(cls, include_experimental: bool = False) -> Iterable[Self]:
        for lang in cls:
            if include_experimental or not lang.is_experimental():
                yield lang

    def is_experimental(self) -> bool:
        """
        Check if the language server is experimental or deprecated.
        """
        return False

    def __str__(self) -> str:
        return self.value

    def get_source_fn_matcher(self) -> FilenameMatcher:
        match self:
            case self.MARKDOWN:
                return FilenameMatcher("*.md", "*.mdx", "*.markdown")
            case _:
                raise ValueError(f"Unhandled language: {self}")


@dataclass
class LanguageServerConfig:
    """
    Configuration parameters
    """

    code_language: Language
    trace_lsp_communication: bool = False
    start_independent_lsp_process: bool = True
    ignored_paths: list[str] = field(default_factory=list)
    """Paths, dirs or glob-like patterns. The matching will follow the same logic as for .gitignore entries"""

    @classmethod
    def from_dict(cls, env: dict):
        """
        Create a MultilspyConfig instance from a dictionary
        """
        import inspect

        return cls(**{k: v for k, v in env.items() if k in inspect.signature(cls).parameters})
