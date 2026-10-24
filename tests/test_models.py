
from datetime import datetime, timezone

import pytest

from webscanner.core import ScannerConfig
from webscanner.models import Finding, Scan, ScanStatus, Severity


def test_finding_creation():
    finding = Finding(
        check_id="missing-csp",
        title="Missing Content-Security-Policy",
        severity=Severity.MEDIUM,
        description="The response does not include a CSP header.",
        remediation="Configure an appropriate Content-Security-Policy header.",
    )

    assert finding.check_id == "missing-csp"
    assert finding.severity == Severity.MEDIUM
    assert finding.evidence is None


def test_scan_starts_as_pending():
    scan = Scan(target_url="https://example.com")

    assert scan.status == ScanStatus.PENDING
    assert scan.findings == []
    assert scan.finished_at is None


def test_scans_have_independent_findings():
    first = Scan(target_url="https://example.com")
    second = Scan(target_url="https://example.org")

    first.findings.append(
        Finding(
            check_id="test-check",
            title="Test finding",
            severity=Severity.LOW,
            description="Test description",
            remediation="Test remediation",
        )
    )

    assert first.findings_count == 1
    assert second.findings_count == 0


def test_scan_completion():
    scan = Scan(target_url="https://example.com")
    scan.complete()

    assert scan.status == ScanStatus.COMPLETED
    assert scan.finished_at is not None
    assert scan.finished_at.tzinfo is not None


def test_scan_failure():
    scan = Scan(target_url="https://example.com")
    scan.fail()

    assert scan.status == ScanStatus.FAILED
    assert scan.finished_at is not None


@pytest.mark.parametrize(
    "kwargs",
    [
        {"request_timeout": 0},
        {"request_timeout": -1},
        {"max_redirects": -1},
        {"request_delay": -1},
        {"max_requests_per_scan": 0},
    ],
)
def test_invalid_config_is_rejected(kwargs):
    with pytest.raises(ValueError):
        ScannerConfig(**kwargs)


def test_config_is_immutable():
    config = ScannerConfig()

    with pytest.raises(AttributeError):
        config.request_timeout = 10.0
