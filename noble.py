import os
import asyncio
import re
from telethon import TelegramClient, events

# بياناتك
api_id = 23882332
api_hash = '1d515ac7bf517374b9ba7c0d8d74b3fd'
bot_token = '8604013302:AAHAZytEsZdTxyBlzn3-DsQuKjxEoc6jSL0'

SOURCE_ID = -1002266265804  # نوبل ستار (المصدر)
TARGET_CHANNEL = 'hvh32'    # القناة الكبيرة (الوجهة)
MY_RIGHTS = "\n\n━━━━━━━━━━━━━━━\n✨ تم النشر بواسطة: **THAMERDEV**"

client = TelegramClient('noble_session', api_id, api_hash)

@client.on(events.NewMessage)
async def handler(event):
    if event.is_private and event.document and event.document.attributes:
        file_name = event.document.attributes[0].file_name
        
        if file_name.lower().endswith('.ipa'):
            status_msg = await event.reply(f"🔍 جاري استخراج الوصف النصي لـ **{file_name}**...")
            
            # تنظيف اسم الملف للبحث (مثلاً: CityOfDragons -> city, dragons)
            clean_name = re.sub(r'([a-z])([A-Z])', r'\1 \2', file_name.rsplit('.', 1)[0])
            clean_name = re.sub(r'[^a-zA-Z0-9]', ' ', clean_name).lower()
            keywords = [w for w in clean_name.split() if len(w) > 2]
            
            final_caption = f"📱 تطبيق: **{file_name}**{MY_RIGHTS}"
            found = False
            
            try:
                # الحساب الشخصي يسحب آخر 1000 رسالة
                async for message in client.iter_messages(SOURCE_ID, limit=1000):
                    # ✅ هنا السحر: نسحب النص (text) أو الكابشن (caption)
                    # هذا اللي قاله لك شات جي بي تي وهو الصح
                    description = message.message or message.caption or ""
                    
                    if description:
                        # مطابقة الكلمات
                        match = False
                        for word in keywords:
                            if word in description.lower():
                                match = True
                                break
                        
                        if match:
                            final_caption = description + MY_RIGHTS
                            found = True
                            break
                            
            except Exception as e:
                print(f"Error: {e}")

            # النشر النهائي
            try:
                await client.send_file(TARGET_CHANNEL, event.message.media, caption=final_caption, parse_mode='md')
                if found:
                    await status_msg.edit(f"✅ تم سحب الوصف بنجاح!")
                else:
                    await status_msg.edit(f"⚠️ لم أجد نصاً مطابقاً في القناة.")
            except Exception as e:
                await status_msg.edit(f"❌ خطأ: {e}")

async def main():
    await client.start(bot_token=bot_token)
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
