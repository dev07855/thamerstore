import os
import asyncio
from telethon import TelegramClient, events

# بياناتك
api_id = 23882332
api_hash = '1d515ac7bf517374b9ba7c0d8d74b3fd'
bot_token = '8604013302:AAHAZytEsZdTxyBlzn3-DsQuKjxEoc6jSL0'

# القناة الكبيرة للنشر
TARGET_CHANNEL = 'hvh32'

# الوصف المحدث بناءً على طلبك
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

client = TelegramClient('noble_session', api_id, api_hash)

@client.on(events.NewMessage)
async def handler(event):
    if event.is_private and event.document and event.document.attributes:
        file_name = event.document.attributes[0].file_name
        
        if file_name.lower().endswith('.ipa'):
            status_msg = await event.reply(f"📤 جاري النشر في القناة...")
            
            # دمج اسم الملف مع الوصف الجديد
            final_caption = f"📱 تطبيق: **{file_name}**\n" + FIXED_DESCRIPTION
            
            try:
                await client.send_file(
                    TARGET_CHANNEL, 
                    event.message.media, 
                    caption=final_caption,
                    parse_mode='md'
                )
                await status_msg.edit(f"✅ تم النشر بنجاح في @{TARGET_CHANNEL}")
            except Exception as e:
                await status_msg.edit(f"❌ خطأ: {e}")

async def main():
    await client.start(bot_token=bot_token)
    print("🚀 بوت THAMERDEV جاهز بالنص الجديد والمصدر الأول...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
