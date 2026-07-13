from dataclasses import dataclass
from typing import Any, Literal, Optional

Tool = Literal['axe-core', 'ibm-equal-access']


@dataclass
class Violation:
    tool: Tool
    rule_id: str
    wcag: list[str]
    description: str
    count: int
    targets: list[str]
    impact: Optional[str] = None
    help_url: Optional[str] = None


@dataclass
class Metadata:
    timestamp: str
    url: str
    browser: str
    browser_version: str
    viewport: Optional[dict[str, int]]
    device: str
    tool: Tool
    tool_version: str
    wcag_tags: Optional[list[str]] = None


@dataclass
class Result:
    metadata: Metadata
    violations: list[Violation]
    raw: Any
