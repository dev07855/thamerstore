import asyncio
import os
from telethon import TelegramClient, events

# بياناتك
api_id = 23882332
api_hash = '1d515ac7bf517374b9ba7c0d8d74b3fd'

# ملاحظة: اسم السشن هنا لازم يكون نفس اسم الملف اللي رفعته (بدون .session)
# لو ملفك اسمه noble_session.session خليه مثل ما هو تحت
SESSION_NAME = 'noble_session'

TARGET_CHANNEL = 'hvh32'
THAMER_ID = 5664150534

# الوصف اللي طلبته
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

client = TelegramClient(SESSION_NAME, api_id, api_hash)

@client.on(events.NewMessage(chats=THAMER_ID))
async def handler(event):
    if event.document:
        file_name = event.document.attributes[0].file_name
        if file_name.lower().endswith('.ipa'):
            # رد سريع للتأكيد
            await event.reply(f"⏳ جاري تحويل {file_name} بلمح البصر...")
            
            try:
                # التحويل المباشر (Forward)
                caption = f"📱 تطبيق: **{file_name}**\n" + FIXED_DESCRIPTION
                await client.send_file(
                    TARGET_CHANNEL, 
                    event.media, 
                    caption=caption,
                    parse_mode='md'
                )
                await event.reply("✅ تم التحويل بنجاح!")
            except Exception as e:
                await event.reply(f"❌ خطأ: {str(e)}")

async def main():
    # التحقق من وجود ملف السشن
    if not os.path.exists(f"{SESSION_NAME}.session"):
        print(f"⚠️ تحذير: ملف {SESSION_NAME}.session غير موجود في المجلد!")
    
    await client.start()
    print("🚀 البوت شغال بنظام السشن الصاروخي...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
