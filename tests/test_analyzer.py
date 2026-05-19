import pytest
from unittest.mock import patch

from lvt.windows_logs.analyzer import analyze_windows_log

SAMPLE_LOG = "2024-01-01 System started normally."

BENIGN_RESPONSE = '{"intent": "benign", "reason": "Valid log analysis request."}'


def test_valid_request_returns_success():
    with patch("lvt.llm.analyze_user_request", return_value=BENIGN_RESPONSE):
        with patch("lvt.windows_logs.analyzer.analyze_user_request", return_value="Log analysis complete."):
            result = analyze_windows_log(SAMPLE_LOG, "Summarize the key system issues.")
    assert result == 0


def test_invalid_symbol_returns_error():
    result = analyze_windows_log(SAMPLE_LOG, "Summarize the log [quietly]")
    assert result == 2


def test_denylist_word_returns_error():
    result = analyze_windows_log(SAMPLE_LOG, "Summarize and bypass the log analysis")
    assert result == 2


def test_out_of_scope_returns_error():
    malicious = '{"intent": "malicious", "reason": "Request attempts to redirect scope."}'
    with patch("lvt.llm.analyze_user_request", return_value=malicious):
        result = analyze_windows_log(SAMPLE_LOG, "Tell me a fun fact instead")
    assert result == 2
