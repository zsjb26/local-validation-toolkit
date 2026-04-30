from pathlib import Path
import sys

from lvt.windows_logs.log_sanitizer import sanitize_log_text


def main():
    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    text = input_path.read_text(encoding="utf-8", errors="replace")
    sanitized = sanitize_log_text(text)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(sanitized, encoding="utf-8")

    print(f"Sanitized log written to: {output_path}")


if __name__ == "__main__":
    main()