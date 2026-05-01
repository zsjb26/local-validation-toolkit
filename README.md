# Local Validation Toolkit (lvt)

Local Validation Toolkit is a Python-based toolkit for Windows log processing and local LLM analysis. It enables AI-assisted workflows using a local model (via LM Studio), including log sanitization for privacy, structured prompt design, and system log analysis with guardrails for adversarial and out-of-scope user inputs.

## Project Focus

This project explores how local LLMs can be safely applied to real-world system data. It emphasizes prompt design, input handling, and guardrails to evaluate model behavior under normal and adversarial user inputs.

## Features

- Local-first LLM experimentation using LM Studio (OpenAI-compatible API)
- Windows system log ingestion and sanitization to remove sensitive data
- Structured prompt design for consistent log analysis and safe behavior
- Request handling for normal, out-of-scope, and adversarial inputs
- Guardrails to reduce unsafe or policy-violating model responses
- Foundation for future evaluation datasets and pass/fail validation

## Quick Start

```bash
pip install -e .
```
### Scan for Sensitive Values
```bash
python .\scripts\scan_log_sensitivity.py <log_path>
```

### Sanitize a Log
```bash
python .\scripts\sanitize_log.py <input_log> <output_log>
```

### Analyze a Sanitized Log Using a Local LLM
```bash
python .\scripts\analyze_windows_log.py `
  --log <sanitized_log> `
  --request "Summarize the key Windows system issues and security-relevant findings."
```

## Notes
- LM Studio must be running locally with an OpenAI-compatible endpoint.
- Raw logs may contain sensitive information; sanitize before analysis or sharing.

