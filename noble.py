import asyncio
from telethon import TelegramClient, events

# بياناتك
api_id = 23882332
api_hash = '1d515ac7bf517374b9ba7c0d8d74b3fd'
bot_token = '8604013302:AAHAZytEsZdTxyBlzn3-DsQuKjxEoc6jSL0'

TARGET_CHANNEL = 'hvh32'
# شلنا شرط المعرف (THAMER_ID) مؤقتاً عشان نتأكد إنه شغال مع الكل
client = TelegramClient(None, api_id, api_hash)

@client.on(events.NewMessage)
async def handler(event):
    # أول ما توصل أي رسالة، اطبع في الـ Logs عشان نشوف
    print(f"📥 وصلت رسالة جديدة من: {event.sender_id}")
    
    if event.document:
        file_name = event.document.attributes[0].file_name
        print(f"📄 الملف المستلم: {file_name}")
        
        if file_name.lower().endswith('.ipa'):
            await event.reply(f"✅ تم استلام {file_name}.. جاري النشر بالقناة")
            try:
                caption = f"ا🚀 **المصدر الأول في تطبيقات IPA**

🔹 **مميزات تعمل:**
- جميع المميزات الأساسية مفعلة.
- باقي المميزات استكشفها بنفسك داخل التطبيق.

⚠️ **ملاحظة:**
أي مشاكل تظهر لا تتردد في التواصل معنا.
عزيزي اذكر المصدر عند تحويل لقناتك 🌹

💎 **خدماتنا:**
يتوفر لدينا متجر البلس وشهادت لتثبيت IPA.
📱 تطبيق: **{file_name}**\n\n🛡️ بواسطة: **THAMERDEV**"
                await client.send_file(TARGET_CHANNEL, event.media, caption=caption)
                print(f"🚀 تم الإرسال للقناة بنجاح!")
            except Exception as e:
                print(f"❌ خطأ أثناء الإرسال: {e}")
                await event.reply(f"❌ فشل النشر: {e}")

async def main():
    await client.start(bot_token=bot_token)
    print("🚀 البوت شغال الحين.. أرسل ملف IPA وشوف الـ Logs")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
