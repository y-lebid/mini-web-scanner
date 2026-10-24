from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from uuid import UUID, uuid4

from webscanner.models.finding import Finding


class ScanStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass(slots=True)
class Scan:
    target_url: str
    id: UUID = field(default_factory=uuid4)
    status: ScanStatus = ScanStatus.PENDING
    started_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    finished_at: datetime | None = None
    findings: list[Finding] = field(default_factory=list)

    def complete(self) -> None:
        self.status = ScanStatus.COMPLETED
        self.finished_at = datetime.now(timezone.utc)

    def fail(self) -> None:
        self.status = ScanStatus.FAILED
        self.finished_at = datetime.now(timezone.utc)

    @property
    def findings_count(self) -> int:
        return len(self.findings)
