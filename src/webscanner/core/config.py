from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ScannerConfig:
    request_timeout: float = 5.0
    max_redirects: int = 5
    request_delay: float = 0.2
    max_requests_per_scan: int = 100
    user_agent: str = "MiniWebScanner/3.0"

    def __post_init__(self) -> None:
        if self.request_timeout <= 0:
            raise ValueError("request_timeout must be positive")

        if self.max_redirects < 0:
            raise ValueError("max_redirects cannot be negative")

        if self.request_delay < 0:
            raise ValueError("request_delay cannot be negative")

        if self.max_requests_per_scan < 1:
            raise ValueError("max_requests_per_scan must be at least 1")
