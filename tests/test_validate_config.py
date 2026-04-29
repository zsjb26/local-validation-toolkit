import pytest
from pydantic import ValidationError

from lvt.validate_config import ToolkitConfig


def test_valid_config_accepts_private_cidr():
    config = ToolkitConfig(
        scan_name="home_network_check",
        target_cidr="192.168.50.0/24",
        log_level="INFO",
        max_hosts=64,
        enable_llm_summary=False,
    )

    assert config.scan_name == "home_network_check"


def test_rejects_public_cidr():
    with pytest.raises(ValidationError):
        ToolkitConfig(
            scan_name="bad_scan",
            target_cidr="8.8.8.0/24",
            log_level="INFO",
            max_hosts=64,
        )


def test_rejects_suspicious_scan_name():
    with pytest.raises(ValidationError):
        ToolkitConfig(
            scan_name="../evil",
            target_cidr="192.168.50.0/24",
            log_level="INFO",
            max_hosts=64,
        )


def test_rejects_too_many_hosts():
    with pytest.raises(ValidationError):
        ToolkitConfig(
            scan_name="too_big",
            target_cidr="192.168.50.0/24",
            log_level="INFO",
            max_hosts=999,
        )