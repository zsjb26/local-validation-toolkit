from openai import OpenAI

DEFAULT_BASE_URL = "http://localhost:1234/v1"
DEFAULT_MODEL = "deepseek-coder-v2-lite-instruct"


def summarize_validation_results(
    validation_text: str,
    model: str = DEFAULT_MODEL,
    base_url: str = DEFAULT_BASE_URL,
) -> str:
    client = OpenAI(
        base_url=base_url,
        api_key="lm-studio",
    )

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

    return response.choices[0].message.content
