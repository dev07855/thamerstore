import asyncio
from telethon import TelegramClient, events

# بياناتك
api_id = 23882332
api_hash = '1d515ac7bf517374b9ba7c0d8d74b3fd'
bot_token = '8604013302:AAHAZytEsZdTxyBlzn3-DsQuKjxEoc6jSL0'

TARGET_CHANNEL = 'hvh32'

# الوصف اللي كنت تبيه (بدون كليشة إعلانية)
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

client = TelegramClient(None, api_id, api_hash)

@client.on(events.NewMessage)
async def handler(event):
    print(f"📥 وصلت رسالة جديدة من: {event.sender_id}")
    
    if event.document:
        attributes = event.document.attributes
        file_name = "تطبيق_جديد"
        
        for attr in attributes:
            if hasattr(attr, 'file_name'):
                file_name = attr.file_name
        
        if file_name.lower().endswith('.ipa'):
            await event.reply(f"⏳ جاري نشر {file_name} بالوصف المعتمد...")
            try:
                # دمج اسم التطبيق مع الوصف الأساسي
                caption = f"📱 تطبيق: **{file_name}**\n" + FIXED_DESCRIPTION
                
                await client.send_file(TARGET_CHANNEL, event.media, caption=caption)
                print(f"🚀 تم الإرسال بنجاح!")
            except Exception as e:
                print(f"❌ خطأ: {e}")
                await event.reply(f"❌ فشل النشر: {e}")

async def main():
    await client.start(bot_token=bot_token)
    print("🚀 البوت شغال بالوصف المعتمد.. بانتظار التحويل!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
