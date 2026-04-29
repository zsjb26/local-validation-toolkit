# Local Validation Toolkit (lvt)

Config-driven validation + security checks with optional local LLM summaries (LM Studio).

## Features

* Pydantic-based config validation
* Security-minded input checks (CIDR, names)
* pytest coverage
* Local LLM summaries via OpenAI-compatible API

## Quick start

```bash
pip install -e .
python -m lvt.validate\_config examples/sample\_config.json
pytest

