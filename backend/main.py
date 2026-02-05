from __future__ import annotations

import logging
import os
from collections import Counter
from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("prompt-poem")

app = FastAPI(title="Prompt Poem API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_MODEL = os.environ.get("OPENAI_MODEL", "gpt-5.1")
_client = OpenAI()


class PoemRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=2000)


class PoemResponse(BaseModel):
    poem: str
    used_words: List[str]
    source: str


_STOP_WORDS = {
    "и",
    "а",
    "но",
    "в",
    "во",
    "на",
    "с",
    "со",
    "к",
    "ко",
    "от",
    "до",
    "за",
    "по",
    "о",
    "об",
    "у",
    "для",
    "про",
    "что",
    "это",
    "как",
    "так",
    "же",
    "бы",
    "ли",
    "мы",
    "вы",
    "они",
    "я",
    "ты",
    "он",
    "она",
    "оно",
    "наш",
    "ваш",
    "их",
    "его",
    "ее",
    "из",
    "над",
    "под",
    "между",
    "быть",
    "есть",
    "будет",
    "будто",
    "то",
}


def _extract_keywords(text: str, limit: int = 8) -> List[str]:
    words = []
    current = []
    for ch in text.lower():
        if ch.isalpha() or ch in {"-", "'"}:
            current.append(ch)
        else:
            if current:
                words.append("".join(current))
                current = []
    if current:
        words.append("".join(current))

    filtered = [w for w in words if len(w) > 2 and w not in _STOP_WORDS]
    if not filtered:
        return []

    counts = Counter(filtered)
    ranked = [w for w, _ in counts.most_common()]
    return ranked[:limit]


def _compose_poem(prompt: str) -> PoemResponse:
    keywords = _extract_keywords(prompt)

    if not keywords:
        poem = (
            "Ты шепнул(а) пустоту — и она отозвалась.\n"
            "Меж строк растет дыхание, как медленный рассвет.\n"
            "Я собираю смысл из хрупких пауз и тишин,\n"
            "И мир становится стихом, когда ты рядом есть."
        )
        return PoemResponse(poem=poem, used_words=[], source="fallback")

    # Build a short free-verse poem with user keywords woven in.
    line1 = f"В словах твоих звучит: {', '.join(keywords[:3])}."
    line2 = (
        f"Я вижу, как {keywords[0]} ищет свет,"
        if len(keywords) > 1
        else f"Я вижу, как {keywords[0]} ищет свет,"
    )
    line3 = (
        f"а {keywords[1]} держит ритм, как тихий берег,"
        if len(keywords) > 2
        else "а ветер держит ритм, как тихий берег,"
    )
    line4 = (
        f"и {keywords[2]} ложится в строки мягким снегом."
        if len(keywords) > 3
        else "и слово ложится в строки мягким снегом."
    )

    tail_words = keywords[3:]
    if tail_words:
        line5 = f"Пусть будут рядом: {', '.join(tail_words)} — как огни."
    else:
        line5 = "Пусть будут рядом простые огни надежды."

    poem = "\n".join([line1, line2, line3, line4, line5])
    return PoemResponse(poem=poem, used_words=keywords, source="fallback")


def _compose_poem_llm(prompt: str) -> PoemResponse:
    keywords = _extract_keywords(prompt)
    keywords_text = ", ".join(keywords) if keywords else "нет"

    instructions = (
        "Ты поэт. Напиши короткий свободный стих на русском (4–8 строк), "
        "используя слова и идеи из промпта. Сохраняй образность и мягкий ритм. "
        "Не добавляй заголовок, не используй списки."
    )
    user_input = f"Промпт: {prompt}\nКлючевые слова: {keywords_text}"

    response = _client.responses.create(
        model=_MODEL,
        instructions=instructions,
        input=user_input,
        max_output_tokens=300,
        temperature=0.8,
    )

    poem = response.output_text.strip()
    if not poem:
        logger.warning("LLM returned empty output; falling back.")
        return _compose_poem(prompt)

    return PoemResponse(poem=poem, used_words=keywords, source="llm")


@app.post("/api/poem", response_model=PoemResponse)
async def generate_poem(payload: PoemRequest) -> PoemResponse:
    try:
        return _compose_poem_llm(payload.prompt)
    except Exception as exc:
        # Fallback to a local generator if the LLM call fails.
        logger.exception("LLM call failed; using fallback.", exc_info=exc)
        return _compose_poem(payload.prompt)


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}
