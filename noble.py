import asyncio
from telethon import TelegramClient, events

# بياناتك
api_id = 23882332
api_hash = '1d515ac7bf517374b9ba7c0d8d74b3fd'
bot_token = '8604013302:AAHAZytEsZdTxyBlzn3-DsQuKjxEoc6jSL0'

TARGET_CHANNEL = 'hvh32'
# قفل الأمان: معرفك الشخصي
THAMER_ID = 5664150534

client = TelegramClient(None, api_id, api_hash)

@client.on(events.NewMessage(chats=THAMER_ID)) # هنا القفل: ما يسمع إلا منك
async def handler(event):
    # طباعة في الـ Logs للتأكد
    print(f"📥 استلمت طلب نشر من ثامر: {event.sender_id}")
    
    if event.document:
        file_name = event.document.attributes[0].file_name
        
        if file_name.lower().endswith('.ipa'):
            await event.reply(f"⏳ جاري النشر لمرة واحدة فقط...")
            try:
                # الوصف اللي طلبته بالضبط
                caption = f"""📱 تطبيق: **{file_name}**

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
✨ تم النشر بواسطة: **THAMERDEV** 🛡️"""

                await client.send_file(TARGET_CHANNEL, event.media, caption=caption)
                print(f"🚀 تم النشر بنجاح!")
            except Exception as e:
                print(f"❌ خطأ: {e}")
                await event.reply(f"❌ فشل النشر: {e}")

async def main():
    await client.start(bot_token=bot_token)
    print("🚀 البوت شغال بنظام الأمان.. مستحيل يكرر النشر!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
