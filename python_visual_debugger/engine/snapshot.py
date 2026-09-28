from dataclasses import dataclass, field
from typing import Any


@dataclass
class Snapshot:
    step: int
    line_number: int
    event: str
    source_line: str = ""
    stdout: str = ""
    changed_vars: dict[str, Any] = field(default_factory=dict)
    variables: dict[str, Any] = field(default_factory=dict)