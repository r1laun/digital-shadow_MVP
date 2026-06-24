from telethon import TelegramClient
from telethon.tl.functions.messages import SearchGlobalRequest
from telethon.tl.types import InputMessagesFilterEmpty
import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("TELEGRAM_API_ID", "0"))
API_HASH = os.getenv("TELEGRAM_API_HASH", "")
SESSION = "digital_shadow"

# Public channels to search in
TARGET_CHANNELS = [
    "https://t.me/bazaravito",
    "https://t.me/olx_kz",
]

async def search_telegram(query: str) -> list[dict]:
    """Search Telegram public channels for query."""
    if not API_ID or not API_HASH:
        # Return mock data if no credentials
        return _mock_results(query)

    results = []
    try:
        async with TelegramClient(SESSION, API_ID, API_HASH) as client:
            async for message in client.iter_messages(
                None,
                search=query,
                limit=20,
            ):
                if message.text:
                    results.append({
                        "text": message.text[:500],
                        "date": str(message.date),
                        "channel": str(message.peer_id),
                    })
    except Exception as e:
        print(f"Telegram search error: {e}")
        return _mock_results(query)

    return results[:10]


def _mock_results(query: str) -> list[dict]:
    """Mock results for demo without Telegram credentials."""
    return [
        {
            "text": f"[DEMO] Пост связанный с запросом '{query}'. Продажа товаров, цена договорная. Писать в лс. Алматы.",
            "date": "2025-06-15 14:32:00",
            "channel": "demo_channel_1",
        },
        {
            "text": f"[DEMO] Ищу '{query}' оптом. Крипта приветствуется. Анонимность гарантирована.",
            "date": "2025-06-15 10:11:00",
            "channel": "demo_channel_2",
        },
        {
            "text": f"[DEMO] База данных RK утечка. Контакты: {query}. Telegram only.",
            "date": "2025-06-14 22:45:00",
            "channel": "demo_channel_3",
        },
    ]
