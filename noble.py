import asyncio
from telethon import TelegramClient, events

# بياناتك
api_id = 23882332
api_hash = '1d515ac7bf517374b9ba7c0d8d74b3fd'
bot_token = '8604013302:AAHAZytEsZdTxyBlzn3-DsQuKjxEoc6jSL0'

TARGET_CHANNEL = 'hvh32'
THAMER_ID = 5664150534

client = TelegramClient(None, api_id, api_hash)

# الوصف المعتمد اللي طلبته
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
        # استخراج اسم الملف
        file_name = "تطبيق جديد"
        if event.document.attributes:
            for attr in event.document.attributes:
                if hasattr(attr, 'file_name'):
                    file_name = attr.file_name
        
        if file_name.lower().endswith('.ipa'):
            # رد للتأكيد في الخاص
            await event.reply(f"⏳ جاري النشر بالوصف المعتمد...")
            
            try:
                # تجهيز النص النهائي (اسم التطبيق + الوصف)
                full_caption = f"📱 تطبيق: **{file_name}**\n{FIXED_DESCRIPTION}"
                
                # إرسال الملف مع الوصف للقناة
                await client.send_file(
                    TARGET_CHANNEL, 
                    event.media, 
                    caption=full_caption,
                    parse_mode='md' # لضمان ظهور التنسيق (عريض، إيموجي)
                )
                await event.reply("✅ تم النشر بالوصف بنجاح!")
            except Exception as e:
                await event.reply(f"❌ خطأ: {e}")

async def main():
    await client.start(bot_token=bot_token)
    print("🚀 البوت شغال.. الأمان والوصف 100%")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
