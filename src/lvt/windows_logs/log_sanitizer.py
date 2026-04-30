import re


SANITIZATION_PATTERNS = {
    "windows_user_path": (
        r"C:\\Users\\[^\\\s]+",
        r"C:\\Users\\<USERNAME>",
    ),
    "sid": (
        r"\bS-\d-\d+(?:-\d+){1,}\b",
        r"<SID>",
    ),
    "email_address": (
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        r"<EMAIL>",
    ),
    "mac_address": (
        r"\b(?:[0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}\b",
        r"<MAC_ADDRESS>",
    ),
}


def sanitize_log_text(text: str) -> str:
    sanitized = text

    for _label, (pattern, replacement) in SANITIZATION_PATTERNS.items():
        sanitized = re.sub(pattern, replacement, sanitized)

    return sanitized