from dataclasses import dataclass
from enum import StrEnum


class Severity(StrEnum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(slots=True)
class Finding:
    check_id: str
    title: str
    severity: Severity
    description: str
    remediation: str
    evidence: str | None = None
    affected_url: str | None = None
