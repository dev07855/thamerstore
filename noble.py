import os
import asyncio
import re
from telethon import TelegramClient, events, Button

# بياناتك
api_id = 23882332
api_hash = '1d515ac7bf517374b9ba7c0d8d74b3fd'
bot_token = '8604013302:AAHAZytEsZdTxyBlzn3-DsQuKjxEoc6jSL0'

TARGET_CHANNEL = 'hvh32'  # قناتك
THAMER_ID = 5664150534    # آيديك الشخصي

stats_db = {}

# تشغيل البوت بالتوكن (عشان تظهر الأزرار)
client = TelegramClient('bot_session', api_id, api_hash).start(bot_token=bot_token)

@client.on(events.NewMessage)
async def thamer_handler(event):
    # الحماية: فقط أنت يا ثامر تقدر ترسل ملف للبوت
    if event.sender_id != THAMER_ID:
        return

    if event.is_private and event.document:
        file_name = event.document.attributes[0].file_name
        
        if file_name.lower().endswith('.ipa'):
            await event.reply(f"⏳ جاري النشر بالأزرار التفاعلية...")

            caption = f"""
🚀 **المصدر الأول في تطبيقات IPA**

📱 تطبيق: **{file_name}**

🔹 **المميزات:** استكشفها بنفسك داخل التطبيق.
⚠️ اذكر المصدر عند تحويل لقناتك 🌹

📊 **تفاعل المتابعين:**
📥 عدد ضغطات التحميل: 0
⭐ تقييم المتابعين: 0

━━━━━━━━━━━━━━━
✨ تم النشر بواسطة: **THAMERDEV**
"""
            # الأزرار (هنا بتظهر لأن المرسل هو البوت)
            buttons = [
                [Button.inline("📥 سجل تحميلك هنا", data=f"dl_{file_name}")],
                [Button.inline("⭐ تقييم 5 نجوم", data=f"rate_{file_name}")]
            ]

            try:
                # النشر بواسطة البوت
                await client.send_file(
                    TARGET_CHANNEL, 
                    event.media, 
                    caption=caption, 
                    buttons=buttons, 
                    parse_mode='md'
                )
                await event.reply(f"✅ تم النشر بنجاح! شيك على القناة وبتلقى الأزرار.")
            except Exception as e:
                await event.reply(f"❌ خطأ: {e}")

@client.on(events.CallbackQuery)
async def callback_handler(event):
    data = event.data.decode('utf-8')
    file_key = data.split("_", 1)[1]
    
    if file_key not in stats_db:
        stats_db[file_key] = {'dl': 0, 'voters': []}

    if data.startswith("dl_"):
        stats_db[file_key]['dl'] += 1
        await event.answer(f"✅ تم تسجيل تحميلك! إجمالي: {stats_db[file_key]['dl']}", alert=False)
    elif data.startswith("rate_"):
        if event.sender_id in stats_db[file_key]['voters']:
            await event.answer("⚠️ قيمت قبل كذا يا بطل!", alert=True)
            return
        stats_db[file_key]['voters'].append(event.sender_id)
        await event.answer("شكراً لتقييمك! ⭐", alert=True)

    # تحديث النص
    try:
        s = stats_db[file_key]
        new_text = re.sub(r"📥 عدد ضغطات التحميل: \d+", f"📥 عدد ضغطات التحميل: {s['dl']}", event.original_update.message.message)
        new_text = re.sub(r"⭐ تقييم المتابعين: \d+", f"⭐ تقييم المتابعين: {len(s['voters'])}", new_text)
        await event.edit(new_text, buttons=event.original_update.message.reply_markup)
    except: pass

print("🚀 بوت ثامر شغال بالأزرار...")
client.run_until_disconnected()
