import asyncio
from telethon import TelegramClient, events

# بياناتك الصافية
api_id = 23882332
api_hash = '1d515ac7bf517374b9ba7c0d8d74b3fd'
bot_token = '8604013302:AAHAZytEsZdTxyBlzn3-DsQuKjxEoc6jSL0'

TARGET_CHANNEL = 'hvh32'
THAMER_ID = 5664150534

# الوصف اللي طلبته (بدون إضافات مني)
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
✨ تم النشر بواسطة: **THAMERDEV**
"""

# تشغيل بدون تعقيد السشن
client = TelegramClient(None, api_id, api_hash)

@client.on(events.NewMessage(chats=THAMER_ID))
async def handler(event):
    if event.document:
        file_name = event.document.attributes[0].file_name
        if file_name.lower().endswith('.ipa'):
            # رد للتأكيد
            await event.reply(f"⏳ جاري النشر...")
            try:
                # التحويل المباشر
                await client.send_file(
                    TARGET_CHANNEL, 
                    event.media, 
                    caption=f"📱 تطبيق: **{file_name}**\n" + FIXED_DESCRIPTION
                )
                await event.reply("✅ تم بنجاح!")
            except Exception as e:
                await event.reply(f"❌ خطأ: {e}")

async def main():
    await client.start(bot_token=bot_token)
    await client.run_until_disconnected()

if __name__ == '__main__':
    # تشغيل آمن ومضمون
    asyncio.run(main())
