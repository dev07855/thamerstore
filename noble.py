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
MY_RIGHTS = "\n\n━━━━━━━━━━━━━━━\n✨ تم النشر بواسطة: **THAMERDEV**"

client = TelegramClient('noble_session', api_id, api_hash)

@client.on(events.NewMessage)
async def handler(event):
    if event.document and event.document.attributes:
        file_name = event.document.attributes[0].file_name
        if file_name.lower().endswith('.ipa'):
            
            status_msg = await event.reply(f"🔍 جاري سحب الوصف الكامل لـ **{file_name}**...")
            
            # نأخذ الحروف فقط من اسم ملفك (infltr)
            clean_name = "".join(re.findall(r'[a-zA-Z]', file_name.rsplit('.', 1)[0])).lower()
            
            final_caption = f"📱 تطبيق: **{file_name}**{MY_RIGHTS}"
            
            try:
                # بحث عميق جداً في آخر 800 منشور
                async for message in client.iter_messages(SOURCE_CHANNEL, limit=800):
                    # سحب كل النصوص الممكنة من المنشور
                    texts = []
                    if message.text: texts.append(message.text.lower())
                    if message.caption: texts.append(message.caption.lower())
                    
                    # إذا المنشور فيه نص
                    if texts:
                        full_msg_text = " ".join(texts)
                        # تنظيف نص أحمد من كل الرموز للمطابقة
                        clean_target = "".join(re.findall(r'[a-zA-Z]', full_msg_text))
                        
                        # مطابقة مرنة: لو اسم ملفك موجود في نص أحمد
                        if clean_name in clean_target or clean_name[:3] in clean_target:
                            # نأخذ النص الأصلي (مو المنظف) عشان نحافظ على العربي والانجليزي
                            actual_desc = message.text or message.caption
                            final_caption = actual_desc + MY_RIGHTS
                            await status_msg.edit(f"✅ تم العثور على الوصف الكامل!")
                            break
            except Exception as e:
                print(f"Error: {e}")

            # النشر الفوري
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
