import argparse
import ipaddress
import json
from pathlib import Path
from typing import Literal

from lvt.llm import summarize_validation_results
from pydantic import BaseModel, Field, ValidationError, field_validator


class ToolkitConfig(BaseModel):
    scan_name: str = Field(min_length=3, max_length=64)
    target_cidr: str
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"]
    max_hosts: int = Field(ge=1, le=256)
    enable_llm_summary: bool = False

    @field_validator("scan_name")
    @classmethod
    def validate_scan_name(cls, value: str) -> str:
        allowed = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-")
        if any(ch not in allowed for ch in value):
            raise ValueError("scan_name may only contain letters, numbers, underscores, and hyphens")
        return value

    @field_validator("target_cidr")
    @classmethod
    def validate_target_cidr(cls, value: str) -> str:
        try:
            network = ipaddress.ip_network(value, strict=False)
        except ValueError as exc:
            raise ValueError("target_cidr must be a valid CIDR range") from exc

        if not network.is_private:
            raise ValueError("target_cidr must be a private/local network range")

        return value


def load_config(path: Path) -> ToolkitConfig:
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    raw = json.loads(path.read_text(encoding="utf-8"))
    return ToolkitConfig.model_validate(raw)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate toolkit config")
    parser.add_argument("config_path", help="Path to JSON config file")
    args = parser.parse_args()

    try:
        config = load_config(Path(args.config_path))
    except (ValidationError, FileNotFoundError, json.JSONDecodeError) as exc:
        print("[FAIL] Config validation failed")
        print(exc)
        return 1

    print("[PASS] Config validation succeeded")
    output = config.model_dump_json(indent=2)
    print(output)
    if config.enable_llm_summary:
        print("\n[LLM_SUMMARY]")

        try:
            summary = summarize_validation_results(output)
            print(summary)
        except Exception as exc:
            print("[LLM ERROR]")
            print(exc)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())