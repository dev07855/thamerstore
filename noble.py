import os
import asyncio
import re
from telethon import TelegramClient, events, Button

# بياناتك
api_id = 23882332
api_hash = '1d515ac7bf517374b9ba7c0d8d74b3fd'
bot_token = '8604013302:AAHAZytEsZdTxyBlzn3-DsQuKjxEoc6jSL0'

TARGET_CHANNEL = 'hvh32'
THAMER_ID = 5664150534  # آيديك يا ثامر

client = TelegramClient('bot_session', api_id, api_hash)

@client.on(events.NewMessage)
async def handler(event):
    # إذا مو أنت اللي أرسلت الملف، البوت بيسكت
    if event.sender_id != THAMER_ID:
        return

    if event.is_private and event.document:
        file_name = event.document.attributes[0].file_name
        
        if file_name.lower().endswith('.ipa'):
            # رسالة فورية للتأكيد
            await event.reply("✅ استلمت الملف يا ثامر، جاري النشر الآن...")

            caption = f"📱 تطبيق: **{file_name}**\n\n🚀 المصدر الأول في تطبيقات IPA\n⚠️ اذكر المصدر عند التحويل\n━━━━━━━━━━━━━━━\n✨ بواسطة: **THAMERDEV**"
            
            # الأزرار التفاعلية
            buttons = [
                [Button.inline("📥 سجل تحميلك هنا", data=f"dl_{file_name}")],
                [Button.inline("⭐ قيم 5 نجوم", data=f"rate_{file_name}")]
            ]

            try:
                await client.send_file(TARGET_CHANNEL, event.media, caption=caption, buttons=buttons, parse_mode='md')
                await event.reply("🔥 تم النشر في القناة بنجاح!")
            except Exception as e:
                await event.reply(f"❌ خطأ في النشر: {e}")

async def main():
    await client.start(bot_token=bot_token)
    await client.run_until_disconnected()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
