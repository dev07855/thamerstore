import os
import asyncio
import re
from telethon import TelegramClient, events

# بياناتك
api_id = 23882332
api_hash = '1d515ac7bf517374b9ba7c0d8d74b3fd'
bot_token = '8604013302:AAHAZytEsZdTxyBlzn3-DsQuKjxEoc6jSL0'

SOURCE_CHANNEL = 'A7maad_dev'
BIG_CHANNEL = 'hvh32'

client = TelegramClient('noble_session', api_id, api_hash)

@client.on(events.NewMessage)
async def handler(event):
    if event.document and event.document.attributes:
        file_name = event.document.attributes[0].file_name
        if file_name.lower().endswith('.ipa'):
            
            # إشعار سريع
            status_msg = await event.reply(f"⚡ **النظام السريع:** جاري معالجة {file_name}...")
            
            # --- جلب الوصف فقط ---
            clean_name = re.sub(r'[^a-zA-Z]', '', file_name.rsplit('.', 1)[0]).lower()
            final_caption = f"📱 تطبيق: {file_name}\n\n(لم يتم العثور على وصف)"
            
            try:
                async for message in client.iter_messages(SOURCE_CHANNEL, limit=200):
                    full_text = (message.text or "") + (message.caption or "")
                    if full_text:
                        clean_full_text = re.sub(r'[^a-zA-Z]', '', full_text).lower()
                        if clean_name[:5] in clean_full_text:
                            final_caption = full_text
                            break
            except: pass

            # --- الخطوة السحرية: إرسال نسخة بدون تحميل ---
            try:
                # نستخدم send_file مع الـ file_id حق الملف الأصلي
                # كذا تليجرام ينقله فوراً بدون ما يمر بسيرفر Render
                await client.send_file(
                    BIG_CHANNEL, 
                    event.message.media, 
                    caption=final_caption
                )
                await status_msg.edit(f"✅ **تم النقل الفوري!**\nالتطبيق صار في قناتك @{BIG_CHANNEL}")
            except Exception as e:
                await status_msg.edit(f"❌ خطأ في النقل: {e}")

async def main():
    await client.start(bot_token=bot_token)
    print("🚀 نظام النقل السريع شغال يا ثامر...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
