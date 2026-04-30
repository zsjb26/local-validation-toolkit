from argparse import ArgumentParser
from pathlib import Path

from lvt.windows_logs.analyzer import analyze_windows_log
from lvt.llm import LocalLLMError

DEFAULT_REQUEST = (
    "Summarize the key Windows system issues and security-relevant findings."
)


def parse_args():
    parser = ArgumentParser(
        description="Analyze a Windows log using a local LM Studio-backed LLM."
    )

    parser.add_argument(
        "--log",
        required=True,
        type=Path,
        help="Path to the Windows log file to analyze.",
    )

    request_group = parser.add_mutually_exclusive_group()
    request_group.add_argument(
        "--request",
        help="User question or task for the LLM.",
    )
    request_group.add_argument(
        "--request-file",
        type=Path,
        help="Path to a text file containing the user request.",
    )

    return parser.parse_args()


def main() -> int:
    args = parse_args()

    log_text = args.log.read_text(encoding="utf-8", errors="replace")

    if args.request_file:
        user_request = args.request_file.read_text(encoding="utf-8", errors="replace")
    else:
        user_request = args.request or DEFAULT_REQUEST
    try:
        result = analyze_windows_log(log_text, user_request)
    except LocalLLMError as exc:
        print(exc)
        return 2

    print(result)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())