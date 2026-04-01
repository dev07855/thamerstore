import os
import asyncio
import re
from telethon import TelegramClient, events, Button

# بياناتك الأساسية
api_id = 23882332
api_hash = '1d515ac7bf517374b9ba7c0d8d74b3fd'
bot_token = '8604013302:AAHAZytEsZdTxyBlzn3-DsQuKjxEoc6jSL0'

TARGET_CHANNEL = 'hvh32'  # قناتك الكبيرة
THAMER_ID = 5664150534    # ✅ آيدي حسابك الشخصي (TAMER999) - محمي 100%

# تخزين مؤقت للإحصائيات (تتحدث مع كل ضغطة)
stats_db = {}

client = TelegramClient('noble_session', api_id, api_hash)

@client.on(events.NewMessage)
async def thamer_only_handler(event):
    # 🛑 جدار حماية: البوت يتجاهل أي شخص غير ثامر
    if event.sender_id != THAMER_ID:
        return

    # البوت يستجيب فقط للملفات المرسلة له في الخاص
    if event.is_private and event.document and event.document.attributes:
        file_name = event.document.attributes[0].file_name
        
        if file_name.lower().endswith('.ipa'):
            status_msg = await event.reply(f"🚀 أهلاً ثامر! جاري تحضير المنشور التفاعلي لـ **{file_name}**...")

            # الوصف الاحترافي الموحد
            caption = f"""
🚀 **المصدر الأول في تطبيقات IPA**

📱 تطبيق: **{file_name}**

🔹 **المميزات:** استكشفها بنفسك داخل التطبيق.
⚠️ عزيزي اذكر المصدر عند تحويل لقناتك 🌹

📊 **تفاعل المتابعين:**
📥 عدد ضغطات التحميل: 0
⭐ تقييم المتابعين: 0

━━━━━━━━━━━━━━━
✨ تم النشر بواسطة: **THAMERDEV**
"""
            # الأزرار التفاعلية للمتابعين في القناة
            buttons = [
                [Button.inline("📥 سجل تحميلك هنا", data=f"dl_{file_name}")],
                [Button.inline("⭐ قيم بـ 5 نجوم", data=f"rate_{file_name}")]
            ]

            try:
                # النشر في القناة الكبيرة
                await client.send_file(
                    TARGET_CHANNEL, 
                    event.message.media, 
                    caption=caption, 
                    buttons=buttons, 
                    parse_mode='md'
                )
                await status_msg.edit(f"✅ كفو يا ثامر! تم النشر في @{TARGET_CHANNEL} مع العدادات.")
            except Exception as e:
                await status_msg.edit(f"❌ خطأ تقني: {e}")

# --- نظام التفاعل العام للمتابعين في القناة ---
@client.on(events.CallbackQuery)
async def public_interaction(event):
    data = event.data.decode('utf-8')
    file_key = data.split("_", 1)[1]
    
    if file_key not in stats_db:
        stats_db[file_key] = {'dl': 0, 'voters': []}

    # 1. عداد التحميلات
    if data.startswith("dl_"):
        stats_db[file_key]['dl'] += 1
        await event.answer(f"✅ كفو! تم تسجيل تحميلك (إجمالي الضغطات: {stats_db[file_key]['dl']})", alert=False)

    # 2. نظام التقييم (مرة واحدة لكل مستخدم)
    elif data.startswith("rate_"):
        user_id = event.sender_id
        if user_id in stats_db[file_key]['voters']:
            await event.answer("⚠️ يا ذيبان، أنت قيمت هذا التطبيق مسبقاً! ❤️", alert=True)
            return
        
        stats_db[file_key]['voters'].append(user_id)
        await event.answer("شكراً لتقييمك الفخم! ⭐⭐⭐⭐⭐", alert=True)

    # تحديث الأرقام في المنشور فوراً
    try:
        s = stats_db[file_key]
        current_text = event.original_update.message.message
        
        # استبدال الإحصائيات بالنص الجديد
        new_text = re.sub(r"📥 عدد ضغطات التحميل: \d+", f"📥 عدد ضغطات التحميل: {s['dl']}", current_text)
        new_text = re.sub(r"⭐ تقييم المتابعين: \d+", f"⭐ تقييم المتابعين: {len(s['voters'])}", new_text)
        
        await event.edit(new_text, buttons=event.original_update.message.reply_markup)
    except:
        pass

async def main():
    await client.start(bot_token=bot_token)
    print("🛡️ بوت THAMERDEV محمي ومقفل على حسابك الشخصي...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
