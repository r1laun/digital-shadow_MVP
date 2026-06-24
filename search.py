import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("TELEGRAM_API_ID", "0"))
API_HASH = os.getenv("TELEGRAM_API_HASH", "")
SESSION = "digital_shadow"

async def search_telegram(query: str) -> list[dict]:
    if not API_ID or not API_HASH:
        return _mock_results(query)
    try:
        from telethon import TelegramClient
        results = []
        async with TelegramClient(SESSION, API_ID, API_HASH) as client:
            async for message in client.iter_messages(None, search=query, limit=15):
                if message.text:
                    try:
                        channel = message.chat.title or str(message.peer_id)
                        username = f"@{message.chat.username}" if message.chat.username else "закрытый канал"
                    except:
                        channel = "неизвестный канал"
                        username = ""
                    results.append({
                        "text": message.text[:600],
                        "date": message.date.strftime("%Y-%m-%d %H:%M"),
                        "channel": channel,
                        "username": username,
                        "link": f"https://t.me/{message.chat.username}/{message.id}" if hasattr(message.chat, 'username') and message.chat.username else ""
                    })
        return results[:10]
    except Exception as e:
        print(f"Telegram error: {e}")
        return _mock_results(query)


def _mock_results(query: str) -> list[dict]:
    return [
        {
            "text": f"Продаём '{query}' оптом и в розницу. Доставка по Алматы. Пишите в лс. Цена договорная. Анонимность.",
            "date": "2026-06-24 11:32",
            "channel": "Барахолка KZ",
            "username": "@bazar_kz_almaty",
            "link": ""
        },
        {
            "text": f"Ищу поставщика '{query}'. Крипта приветствуется (USDT TRC20). Серьёзные предложения only. Алматы/Астана.",
            "date": "2026-06-24 09:15",
            "channel": "Объявления Казахстан",
            "username": "@ob_kz",
            "link": ""
        },
        {
            "text": f"СЛИВ: база данных РК содержит записи по теме '{query}'. Контакт через бот. -50% первым 10 покупателям.",
            "date": "2026-06-23 22:45",
            "channel": "Dark Market KZ",
            "username": "@dmkz_official",
            "link": ""
        },
    ]
