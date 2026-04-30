from pathlib import Path
import re

LOG_PATH = Path("examples/sample_logs/windows_system_sample.txt")

PATTERNS = {
    "ipv4_address": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
    "email_address": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
    "windows_path_user": r"C:\\Users\\[^\\\s]+",
    "possible_hostname": r"\b(?:DESKTOP|LAPTOP|WIN|PC)-[A-Z0-9]+\b",
    "possible_username_field": r"(?i)\b(account name|user name|username|subject user name)\s*:\s*[^\r\n]+",
    "domain_field": r"(?i)\b(account domain|domain)\s*:\s*[^\r\n]+",
    "sid": r"\bS-\d-\d+(?:-\d+){1,}\b",
    "mac_address": r"\b(?:[0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}\b",
    "guid": r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b",
    "possible_secret": r"(?i)\b(password|passwd|pwd|secret|token|api[_-]?key|credential|bearer)\b",
}

def scan_text(text: str) -> list[dict]:
    findings = []

    for label, pattern in PATTERNS.items():
        for match in re.finditer(pattern, text):
            start = max(match.start() - 60, 0)
            end = min(match.end() + 60, len(text))
            findings.append({
                "type": label,
                "match": match.group(0),
                "context": text[start:end].replace("\n", " ")
            })

    return findings

def main():
    if not LOG_PATH.exists():
        raise FileNotFoundError(f"Missing log file: {LOG_PATH}")

    text = LOG_PATH.read_text(encoding="utf-8", errors="replace")
    findings = scan_text(text)

    if not findings:
        print("No obvious sensitive values found.")
        return

    print(f"Found {len(findings)} potential sensitive value(s):\n")

    for item in findings:
        print(f"[{item['type']}] {item['match']}")
        print(f"Context: {item['context']}")
        print("-" * 80)

if __name__ == "__main__":
    main()