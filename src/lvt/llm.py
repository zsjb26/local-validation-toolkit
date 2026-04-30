from openai import APIConnectionError, APIError, OpenAI

DEFAULT_BASE_URL = "http://localhost:1234/v1"
DEFAULT_MODEL = "deepseek-coder-v2-lite-instruct"


class LocalLLMError(RuntimeError):
    """Raised when the local LLM request cannot be completed safely."""


def summarize_validation_results(
    validation_text: str,
    model: str = DEFAULT_MODEL,
    base_url: str = DEFAULT_BASE_URL,
) -> str:
    """
    Send a prompt to the local LM Studio-backed LLM and return the response.

    Raises:
        LocalLLMError: if the request fails or returns invalid output.
    """
    client = OpenAI(
        base_url=base_url,
        api_key="lm-studio",  # placeholder for local LM Studio
    )

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are helping review validation output for a local "
                        "security-minded QA automation toolkit. Be concise. "
                        "Summarize risks, likely causes, and suggested next tests."
                    ),
                },
                {
                    "role": "user",
                    "content": validation_text,
                },
            ],
            temperature=0.2,
        )
    except APIConnectionError as exc:
        raise LocalLLMError(
            "Local LLM service is unavailable. Start the local model server and try again."
        ) from exc
    except APIError as exc:
        raise LocalLLMError(
            "Local LLM request failed. Check the local model server and try again."
        ) from exc
    except Exception as exc:
        # Catch-all to avoid leaking implementation details
        raise LocalLLMError(
            "Local LLM request failed due to an unexpected error."
        ) from exc

    content = response.choices[0].message.content

    if not content or not content.strip():
        raise LocalLLMError("Local LLM returned an empty response.")

    return content.strip()