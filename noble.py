import os
import asyncio
import re
from telethon import TelegramClient, events

# بياناتك
api_id = 23882332
api_hash = '1d515ac7bf517374b9ba7c0d8d74b3fd'
bot_token = '8604013302:AAHAZytEsZdTxyBlzn3-DsQuKjxEoc6jSL0'

# القنوات (تعديل المصدر)
SOURCE_CHANNEL = 'NOPELSTAR'  # السحب من نوبل ستار
BIG_CHANNEL = 'hvh32'         # النشر في القناة الكبيرة

# حقوقك الفخمة
MY_RIGHTS = "\n\n━━━━━━━━━━━━━━━\n✨ تم النشر بواسطة: **THAMERDEV**"

client = TelegramClient('noble_session', api_id, api_hash)

@client.on(events.NewMessage)
async def handler(event):
    if event.document and event.document.attributes:
        file_name = event.document.attributes[0].file_name
        if file_name.lower().endswith('.ipa'):
            
            status_msg = await event.reply(f"🔍 جاري سحب الوصف من @{SOURCE_CHANNEL}...")
            
            # تنظيف اسم ملفك (مثال: infltr)
            clean_name = "".join(re.findall(r'[a-zA-Z]', file_name.rsplit('.', 1)[0])).lower()
            # بحث مرن جداً بأول 3 حروف (عشان لو فيه رموز أو شرطات)
            search_query = clean_name[:3] 
            
            final_caption = f"📱 تطبيق: **{file_name}**{MY_RIGHTS}"
            
            try:
                # البحث في آخر 800 رسالة في نوبل ستار
                async for message in client.iter_messages(SOURCE_CHANNEL, limit=800):
                    # سحب النص سواء كان رسالة أو كابشن تحت صورة
                    description_text = message.message or message.caption or ""
                    
                    if description_text:
                        # تنظيف النص للمطابقة
                        clean_target = "".join(re.findall(r'[a-zA-Z]', description_text)).lower()
                        
                        # إذا لقى تشابه في الاسم (حتى لو فيه رموز)
                        if search_query in clean_target:
                            # ✅ يسحب الوصف كامل (عربي وانجليزي ومميزات)
                            final_caption = description_text + MY_RIGHTS
                            await status_msg.edit(f"✅ كفو! لقيت الوصف في نوبل ستار.")
                            break
            except Exception as e:
                print(f"Error: {e}")

            # --- النقل الفوري للقناة الكبيرة ---
            try:
                await client.send_file(
                    BIG_CHANNEL, 
                    event.message.media, 
                    caption=final_caption,
                    parse_mode='md'
                )
                await status_msg.edit(f"✅ تم النقل بنجاح إلى @{BIG_CHANNEL}")
            except Exception as e:
                await status_msg.edit(f"❌ خطأ أثناء الإرسال: {e}")

async def main():
    await client.start(bot_token=bot_token)
    print("🚀 بوت السحب من نوبل ستار جاهز...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
