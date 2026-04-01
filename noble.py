import asyncio
from telethon import TelegramClient, events

# بياناتك الأساسية
api_id = 23882332
api_hash = '1d515ac7bf517374b9ba7c0d8d74b3fd'
bot_token = '8604013302:AAHAZytEsZdTxyBlzn3-DsQuKjxEoc6jSL0'

TARGET_CHANNEL = 'hvh32'
THAMER_ID = 5664150534

# الوصف اللي اخترته أنت يا ثامر
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

client = TelegramClient('bot_session', api_id, api_hash)

@client.on(events.NewMessage(chats=THAMER_ID))
async def handler(event):
    if event.is_private and event.document:
        file_name = event.document.attributes[0].file_name
        
        if file_name.lower().endswith('.ipa'):
            # رسالة انتظار بسيطة
            status = await event.reply(f"⏳ جاري نشر {file_name}...")
            
            # دمج اسم التطبيق مع الوصف الموحد
            final_caption = f"📱 تطبيق: **{file_name}**\n" + FIXED_DESCRIPTION
            
            try:
                await client.send_file(
                    TARGET_CHANNEL, 
                    event.media, 
                    caption=final_caption,
                    parse_mode='md'
                )
                await status.edit("✅ تم النشر بنجاح في القناة.")
            except Exception as e:
                await status.edit(f"❌ خطأ أثناء النشر: {str(e)}")

async def main():
    await client.start(bot_token=bot_token)
    print("🚀 البوت شغال بالوصف الموحد وبدون أخطاء...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    # تشغيل آمن ومستقر يتوافق مع بايثون 3.14
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
