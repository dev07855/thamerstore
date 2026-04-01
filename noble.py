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

# الحقوق الجديدة اللي طلبتها
MY_RIGHTS = "\n\n━━━━━━━━━━━━━━━\n✨ تم النشر بواسطة: **THAMERDEV**"

client = TelegramClient('noble_session', api_id, api_hash)

@client.on(events.NewMessage)
async def handler(event):
    if event.document and event.document.attributes:
        file_name = event.document.attributes[0].file_name
        if file_name.lower().endswith('.ipa'):
            
            # إشعار البدء
            status_msg = await event.reply(f"🔍 جاري سحب الوصف الكامل لـ **{file_name}**...")
            
            # تنظيف اسم الملف للبحث (نأخذ أول 4 حروف فقط لضمان النتيجة)
            clean_name = "".join(re.findall(r'[a-zA-Z]', file_name.rsplit('.', 1)[0])).lower()
            search_query = clean_name[:4] 
            
            final_caption = f"📱 تطبيق: **{file_name}**{MY_RIGHTS}"
            
            try:
                # البحث في آخر 500 رسالة عند أحمد
                async for message in client.iter_messages(SOURCE_CHANNEL, limit=500):
                    # سحب النص سواء كان رسالة نصية أو كابشن تحت صورة
                    full_text = (message.text or "") + (message.caption or "")
                    
                    if full_text:
                        # تنظيف نص أحمد للمطابقة (نتجاهل الشرطات والرموز)
                        clean_target = "".join(re.findall(r'[a-zA-Z]', full_text)).lower()
                        
                        if search_query in clean_target:
                            # ✅ هنا نسحب كل الوصف (العربي والانجليزي والمميزات)
                            final_caption = full_text + MY_RIGHTS
                            await status_msg.edit(f"✅ تم العثور على الوصف الكامل بنجاح!")
                            break
            except Exception as e:
                print(f"Error: {e}")

            # --- عملية النقل السريع ---
            try:
                await client.send_file(
                    BIG_CHANNEL, 
                    event.message.media, 
                    caption=final_caption,
                    parse_mode='md'
                )
                await status_msg.edit(f"✅ تم النشر في قناتك بواسطة **THAMERDEV**")
            except Exception as e:
                await status_msg.edit(f"❌ خطأ: {e}")

async def main():
    await client.start(bot_token=bot_token)
    print("🚀 بوت THAMERDEV شغال الآن...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
