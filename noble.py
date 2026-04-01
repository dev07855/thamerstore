طfrom telethon import TelegramClient, events, Button
import asyncio

# بياناتك
api_id = 23882332
api_hash = '1d515ac7bf517374b9ba7c0d8d74b3fd'
bot_token = '8604013302:AAHAZytEsZdTxyBlzn3-DsQuKjxEoc6jSL0'

TARGET_CHANNEL = 'hvh32'
THAMER_ID = 5664150534

# تشغيل العميل
client = TelegramClient('bot_session', api_id, api_hash)

@client.on(events.NewMessage(chats=THAMER_ID))
async def handler(event):
    if event.document:
        file_name = event.document.attributes[0].file_name
        if file_name.lower().endswith('.ipa'):
            # أول ما يوصل الملف بيرد عليك فوراً
            await event.reply(f"✅ أبشر يا ثامر، جاري رفع ونشر: {file_name}")

            caption = f"📱 تطبيق: **{file_name}**\n\n🚀 المصدر الأول في تطبيقات IPA\n⚠️ اذكر المصدر عند التحويل\n━━━━━━━━━━━━━━━\n✨ بواسطة: **THAMERDEV**"
            
            buttons = [
                [Button.inline("📥 سجل تحميلك هنا", data="ignore")],
                [Button.inline("⭐ قيم بـ 5 نجوم", data="ignore")]
            ]

            try:
                await client.send_file(TARGET_CHANNEL, event.media, caption=caption, buttons=buttons)
                await event.reply("🔥 تم النشر في القناة بنجاح!")
            except Exception as e:
                await event.reply(f"❌ فشل النشر: {str(e)}")

@client.on(events.CallbackQuery)
async def callback(event):
    await event.answer("✅ تم تسجيل تفاعلك!")

# التشغيل النهائي
print("🚀 البوت حي الآن واستجابته سريعة...")
client.start(bot_token=bot_token)
client.run_until_disconnected()
