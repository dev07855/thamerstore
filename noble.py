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

# الحقوق اللي طلبتها
MY_RIGHTS = "\n\n━━━━━━━━━━━━━━━\n✨ تم النشر بواسطة: **THAMERDEV**"

client = TelegramClient('noble_session', api_id, api_hash)

@client.on(events.NewMessage)
async def handler(event):
    if event.document and event.document.attributes:
        file_name = event.document.attributes[0].file_name
        if file_name.lower().endswith('.ipa'):
            
            status_msg = await event.reply(f"🔍 جاري سحب الوصف الكامل لـ **{file_name}**...")
            
            # تنظيف اسم الملف (نأخذ الحروف فقط)
            clean_name = "".join(re.findall(r'[a-zA-Z]', file_name.rsplit('.', 1)[0])).lower()
            # البحث بأول 3 حروف فقط (عشان يلقط الاسم حتى لو أحمد حاط رموز أو شرطات)
            search_query = clean_name[:3] 
            
            final_caption = f"📱 تطبيق: **{file_name}**{MY_RIGHTS}"
            
            try:
                # البحث في آخر 700 رسالة (بحث عميق جداً)
                async for message in client.iter_messages(SOURCE_CHANNEL, limit=700):
                    # سحب النص من الكابشن (تحت الصورة) أو الرسالة العادية
                    full_text = (message.text or "") + (message.caption or "")
                    
                    if full_text:
                        # تحويل نص أحمد لحروف صغيرة للمطابقة
                        target_text = full_text.lower()
                        
                        # إذا لقى أول 3 حروف من اسم ملفك داخل نص أحمد
                        if search_query in target_text:
                            # ✅ يسحب الوصف كامل (العربي والإنجليزي)
                            final_caption = full_text + MY_RIGHTS
                            await status_msg.edit(f"✅ كفو! لقيت الوصف (صورة/نص)")
                            break
            except Exception as e:
                print(f"Error: {e}")

            # النشر السريع بالوصف الجديد
            try:
                await client.send_file(
                    BIG_CHANNEL, 
                    event.message.media, 
                    caption=final_caption,
                    parse_mode='md'
                )
                await status_msg.edit(f"✅ تم النشر بنجاح بواسطة **THAMERDEV**")
            except Exception as e:
                await status_msg.edit(f"❌ خطأ: {e}")

async def main():
    await client.start(bot_token=bot_token)
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
