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
# حقوقك بشكل مرتب
MY_RIGHTS = "\n\n━━━━━━━━━━━━━━━\n✨ تم النشر بواسطة: [نوبل ستار](https://t.me/hvh32)"

client = TelegramClient('noble_session', api_id, api_hash)

@client.on(events.NewMessage)
async def handler(event):
    # التحقق من وجود ملف IPA
    if event.document and event.document.attributes:
        file_name = event.document.attributes[0].file_name
        if file_name.lower().endswith('.ipa'):
            
            status_msg = await event.reply(f"🔍 **جاري سحب الوصف الكامل لـ {file_name}...**")
            
            # تنظيف اسم الملف للبحث (أخذ الحروف فقط)
            clean_name = "".join(re.findall(r'[a-zA-Z]', file_name.rsplit('.', 1)[0])).lower()
            search_query = clean_name[:5] 
            
            # الوصف الافتراضي في حال لم يجد شيئاً
            final_caption = f"📱 تطبيق: **{file_name}**{MY_RIGHTS}"
            
            try:
                # البحث في آخر 400 منشور عند أحمد
                async for message in client.iter_messages(SOURCE_CHANNEL, limit=400):
                    # دمج النص سواء كان رسالة عادية أو كابشن تحت صورة
                    full_text = (message.text or "") + (message.caption or "")
                    
                    if full_text:
                        # تنظيف نص أحمد للمطابقة
                        clean_target = "".join(re.findall(r'[a-zA-Z]', full_text)).lower()
                        
                        if search_query in clean_target:
                            # ✅ هنا السحر: نأخذ النص الكامل كما هو عند أحمد
                            final_caption = full_text + MY_RIGHTS
                            await status_msg.edit(f"✅ تم العثور على الوصف الكامل!")
                            break
            except Exception as e:
                print(f"Error searching description: {e}")

            # --- عملية النقل الفوري مع الوصف الكامل ---
            try:
                await client.send_file(
                    BIG_CHANNEL, 
                    event.message.media, # إرسال نفس الملف الأصلي
                    caption=final_caption,
                    parse_mode='md' # يدعم الروابط والخط العريض
                )
                await status_msg.edit(f"✅ **تم النشر بالوصف الكامل بنجاح!**")
            except Exception as e:
                await status_msg.edit(f"❌ خطأ أثناء النقل: {e}")

async def main():
    await client.start(bot_token=bot_token)
    print("🚀 بوت الوصف الكامل شغال يا ثامر...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
