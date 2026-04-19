import asyncio
from hydrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN

app = Client(
    "dsrbotz_mx_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=999,
    plugins=dict(root="plugins"),
)

if __name__ == "__main__":
    print("🚀 DsrBotz MX Player Bot Starting...")
    app.run()
