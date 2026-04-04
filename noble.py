import asyncio
from telethon import TelegramClient, events

# بياناتك
api_id = 23882332
api_hash = '1d515ac7bf517374b9ba7c0d8d74b3fd'
bot_token = '8604013302:AAHAZytEsZdTxyBlzn3-DsQuKjxEoc6jSL0'

TARGET_CHANNEL = 'hvh32'
THAMER_ID = 5664150534

client = TelegramClient(None, api_id, api_hash)

# الوصف المعتمد - تأكدت إنه مقفل صح
FIXED_DESCRIPTION = """
🚀 **المصدر الأول في تطبيقات IPA**

🔹 **مميزات تعمل:**
- جميع المميزات الأساسية مفعلة.
- باقي المميزات استكشفها بنفسك داخل التطبيق.

⚠️ **ملاحظة:**
أي مشاكل تظهر لا تتردد في التواصل معنا.
عزيزي اذكر المصدر عند تحويل لقناتك 🌹

💎 **خدماتنا:**
يتوفر لدينا متجر البلس وشهادات لتثبيت IPA.

━━━━━━━━━━━━━━━
✨ تم النشر بواسطة: **THAMERDEV** 🛡️
"""

@client.on(events.NewMessage(chats=THAMER_ID))
async def handler(event):
    if event.document:
        file_name = "تطبيق جديد"
        for attr in event.document.attributes:
            if hasattr(attr, 'file_name'):
                file_name = attr.file_name
        
        if file_name.lower().endswith('.ipa'):
            await event.reply(f"⏳ جاري النشر...")
            try:
                caption = f"📱 تطبيق: **{file_name}**\n" + FIXED_DESCRIPTION
                await client.send_file(TARGET_CHANNEL, event.media, caption=caption)
                await event.reply("✅ تم بنجاح!")
            except Exception as e:
                await event.reply(f"❌ خطأ: {e}")

async def main():
    await client.start(bot_token=bot_token)
    print("🚀 البوت شغال وجاهز!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
