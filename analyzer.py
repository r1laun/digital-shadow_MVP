import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY", ""))

SYSTEM_PROMPT = """Ты — система анализа угроз OSINT для правоохранительных органов Казахстана.
Анализируй текст постов и определяй угрозы.

Отвечай ТОЛЬКО в формате JSON:
{
  "category": "одно из: наркотики | вейпы/алкоголь | дропы | утечка_БД | крипто-мошенничество | нет_угрозы",
  "risk_level": "одно из: низкий | средний | высокий | критический",
  "risk_score": число от 0 до 100,
  "summary": "краткое описание угрозы на русском, 1-2 предложения",
  "entities": ["список", "ключевых", "сущностей", "из текста"],
  "recommendation": "рекомендация для оперативника"
}"""

async def analyze_threat(query: str, posts: list[dict]) -> dict:
    """Analyze posts for threats using Groq AI."""
    if not posts:
        return _empty_result()

    posts_text = "\n\n".join([
        f"Пост {i+1}: {p['text']}" for i, p in enumerate(posts[:5])
    ])

    user_message = f"""Запрос оперативника: "{query}"

Найденные посты:
{posts_text}

Проанализируй и верни JSON."""

    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
            temperature=0.1,
            max_tokens=500,
        )

        raw = response.choices[0].message.content.strip()
        # Strip markdown if present
        if "```" in raw:
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        
        result = json.loads(raw)
        result["posts_count"] = len(posts)
        result["query"] = query
        return result

    except Exception as e:
        print(f"Groq error: {e}")
        return _fallback_result(query, posts)


def _empty_result() -> dict:
    return {
        "category": "нет_угрозы",
        "risk_level": "низкий",
        "risk_score": 0,
        "summary": "Данные не найдены.",
        "entities": [],
        "recommendation": "Нет действий.",
        "posts_count": 0,
    }


def _fallback_result(query: str, posts: list) -> dict:
    """Simple keyword-based fallback if Groq fails."""
    text = " ".join([p["text"].lower() for p in posts])
    
    if any(w in text for w in ["наркот", "закладк", "соль", "мефед"]):
        cat, risk, score = "наркотики", "критический", 95
    elif any(w in text for w in ["вейп", "электронн", "сигарет", "алкогол"]):
        cat, risk, score = "вейпы/алкоголь", "высокий", 75
    elif any(w in text for w in ["drop", "дроп", "карт", "обнал"]):
        cat, risk, score = "дропы", "высокий", 80
    elif any(w in text for w in ["база", "утечка", "слив", "данные"]):
        cat, risk, score = "утечка_БД", "критический", 90
    elif any(w in text for w in ["btc", "usdt", "крипт", "кошелёк"]):
        cat, risk, score = "крипто-мошенничество", "средний", 60
    else:
        cat, risk, score = "нет_угрозы", "низкий", 10

    return {
        "category": cat,
        "risk_level": risk,
        "risk_score": score,
        "summary": f"Обнаружены признаки активности по запросу '{query}'.",
        "entities": [query],
        "recommendation": "Требуется дополнительная проверка.",
        "posts_count": len(posts),
        "query": query,
    }
