import json
import time
from typing import Any

import openai

from ..config import settings
from ..prompt_templates import build_ai_prompt


openai.api_key = settings.OPENAI_API_KEY


def call_openai_prompt(prompt: str) -> str:
    for attempt in range(settings.OPENAI_RETRY_COUNT + 1):
        try:
            response = openai.ChatCompletion.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are a senior digital strategy consultant."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=settings.OPENAI_MAX_TOKENS,
                temperature=0.8,
            )
            return response.choices[0].message.content.strip()
        except Exception:
            if attempt == settings.OPENAI_RETRY_COUNT:
                raise
            time.sleep(2 ** attempt)
    raise RuntimeError("OpenAI request failed after retries.")


def generate_company_analysis(company_name: str, website_url: str, email: str, website_data: dict[str, str]) -> dict[str, str]:
    prompt = build_ai_prompt(company_name, website_url, email, website_data)
    analysis_text = call_openai_prompt(prompt)

    try:
        parsed = json.loads(analysis_text)
        return {
            "executive_summary": parsed.get("executive_summary", ""),
            "business_model": parsed.get("business_model", ""),
            "digital_maturity": parsed.get("digital_maturity", ""),
            "ux_observations": parsed.get("ux_observations", ""),
            "seo_observations": parsed.get("seo_observations", ""),
            "growth_recommendations": parsed.get("growth_recommendations", ""),
            "ai_opportunities": parsed.get("ai_opportunities", ""),
            "conclusion": parsed.get("conclusion", ""),
        }
    except json.JSONDecodeError:
        return {
            "executive_summary": analysis_text,
            "business_model": "See the executive summary for the most relevant business model observations.",
            "digital_maturity": "Insufficient structured output from the AI response.",
            "ux_observations": "Insufficient structured output from the AI response.",
            "seo_observations": "Insufficient structured output from the AI response.",
            "growth_recommendations": "Insufficient structured output from the AI response.",
            "ai_opportunities": "Insufficient structured output from the AI response.",
            "conclusion": "Insufficient structured output from the AI response.",
        }
