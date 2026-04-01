import os
import asyncio
import re
from telethon import TelegramClient, events, Button

# بياناتك
api_id = 23882332
api_hash = '1d515ac7bf517374b9ba7c0d8d74b3fd'
bot_token = '8604013302:AAHAZytEsZdTxyBlzn3-DsQuKjxEoc6jSL0'

TARGET_CHANNEL = 'hvh32'  # قناتك
THAMER_ID = 5664150534    # آيديك

# قاعدة بيانات مؤقتة للعدادات
stats_db = {}

# إنشاء العميل بالطريقة التقليدية المستقرة
client = TelegramClient('bot_session', api_id, api_hash)

@client.on(events.NewMessage)
async def handler(event):
    # فقط ثامر يقدر ينشر
    if event.sender_id != THAMER_ID:
        return

    if event.is_private and event.document:
        file_name = event.document.attributes[0].file_name
        
        if file_name.lower().endswith('.ipa'):
            # رسالة انتظار
            status = await event.reply("⏳ جاري النشر بالأزرار التفاعلية...")

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
            # الأزرار التفاعلية
            buttons = [
                [Button.inline("📥 سجل تحميلك هنا", data=f"dl_{file_name}")],
                [Button.inline("⭐ قيم بـ 5 نجوم", data=f"rate_{file_name}")]
            ]

            try:
                # النشر في القناة
                await client.send_file(
                    TARGET_CHANNEL, 
                    event.media, 
                    caption=caption, 
                    buttons=buttons, 
                    parse_mode='md'
                )
                await status.edit("✅ تم النشر بنجاح مع الأزرار!")
            except Exception as e:
                await status.edit(f"❌ خطأ: {e}")

@client.on(events.CallbackQuery)
async def callback(event):
    data = event.data.decode('utf-8')
    file_key = data.split("_", 1)[1]
    
    if file_key not in stats_db:
        stats_db[file_key] = {'dl': 0, 'voters': []}

    if data.startswith("dl_"):
        stats_db[file_key]['dl'] += 1
        await event.answer(f"✅ تم تسجيل تحميلك! (إجمالي: {stats_db[file_key]['dl']})")
    elif data.startswith("rate_"):
        if event.sender_id in stats_db[file_key]['voters']:
            await event.answer("⚠️ قيمت قبل كذا!", alert=True)
            return
        stats_db[file_key]['voters'].append(event.sender_id)
        await event.answer("شكراً لتقييمك! ⭐", alert=True)

    # تحديث النص في القناة
    try:
        s = stats_db[file_key]
        msg_text = event.original_update.message.message
        new_text = re.sub(r"📥 عدد ضغطات التحميل: \d+", f"📥 عدد ضغطات التحميل: {s['dl']}", msg_text)
        new_text = re.sub(r"⭐ تقييم المتابعين: \d+", f"⭐ تقييم المتابعين: {len(s['voters'])}", new_text)
        await event.edit(new_text, buttons=event.original_update.message.reply_markup)
    except:
        pass

# التشغيل الصحيح لـ Render
async def main():
    await client.start(bot_token=bot_token)
    print("🚀 البوت شغال تمام...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
