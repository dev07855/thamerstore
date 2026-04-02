import asyncio
from telethon import TelegramClient, events

# بياناتك
api_id = 23882332
api_hash = '1d515ac7bf517374b9ba7c0d8d74b3fd'
bot_token = '8604013302:AAHAZytEsZdTxyBlzn3-DsQuKjxEoc6jSL0'

TARGET_CHANNEL = 'hvh32'
THAMER_ID = 5664150534

client = TelegramClient(None, api_id, api_hash)

@client.on(events.NewMessage(chats=THAMER_ID))
async def handler(event):
    if event.document:
        file_name = event.document.attributes[0].file_name
        if file_name.lower().endswith('.ipa'):
            await event.reply(f"⏳ جاري النشر...")
            try:
                caption = f"📱 تطبيق: **{file_name}**\n\n🛡️ بواسطة: **THAMERDEV**"
                await client.send_file(TARGET_CHANNEL, event.media, caption=caption)
                await event.reply("✅ تم بنجاح!")
            except Exception as e:
                await event.reply(f"❌ خطأ: {e}")

async def main():
    await client.start(bot_token=bot_token)
    print("🚀 البوت شغال ونظيف.. بانتظار ملفات الـ IPA")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
