import os
import asyncio
import re
from telethon import TelegramClient, events

# بياناتك
api_id = 23882332
api_hash = '1d515ac7bf517374b9ba7c0d8d74b3fd'
bot_token = '8604013302:AAHAZytEsZdTxyBlzn3-DsQuKjxEoc6jSL0'

# القنوات
SOURCE_CHANNEL = 'NOPELSTAR'  # قناتك اللي فيها الوصف المرتب
BIG_CHANNEL = 'hvh32'         # قناتك الكبيرة للنشر

# حقوقك
MY_RIGHTS = "\n\n━━━━━━━━━━━━━━━\n✨ تم النشر بواسطة: **THAMERDEV**"

client = TelegramClient('noble_session', api_id, api_hash)

@client.on(events.NewMessage)
async def handler(event):
    if event.document and event.document.attributes:
        file_name = event.document.attributes[0].file_name
        if file_name.lower().endswith('.ipa'):
            
            status_msg = await event.reply(f"🔍 جاري سحب الوصف المرتب لـ **{file_name}**...")
            
            # 1. تنظيف اسم الملف وتقسيمه (مثلاً City of Dragons)
            # بيشيل الرموز ويقسم الكلمات حتى لو كانت لازقة مثل CityOfDragons
            clean_name = re.sub(r'([a-z])([A-Z])', r'\1 \2', file_name.rsplit('.', 1)[0]) # فك الكلمات الملتصقة
            clean_name = re.sub(r'[^a-zA-Z0-9]', ' ', clean_name)
            keywords = [word.lower() for word in clean_name.split() if len(word) > 2]
            
            final_caption = f"📱 تطبيق: **{file_name}**{MY_RIGHTS}"
            found = False
            
            try:
                # البحث في آخر 800 رسالة في نوبل ستار
                async for message in client.iter_messages(SOURCE_CHANNEL, limit=800):
                    full_text = (message.text or "") + (message.caption or "")
                    
                    if full_text:
                        # المطابقة: لازم نلقى أول كلمتين من اسم الملف داخل المنشور
                        match_count = 0
                        for word in keywords[:3]: # فحص أول 3 كلمات من الاسم
                            if word in full_text.lower():
                                match_count += 1
                        
                        # إذا لقى تطابق قوي (كلمتين أو أكثر)
                        if match_count >= 1:
                            final_caption = full_text + MY_RIGHTS
                            found = True
                            break
            except Exception as e:
                print(f"Error: {e}")

            if found:
                await status_msg.edit(f"✅ تم سحب الوصف بنجاح من نوبل ستار!")
            else:
                await status_msg.edit(f"⚠️ لم أجد وصفاً مطابقاً بدقة، سيتم النشر بالاسم فقط.")

            # النقل الفوري للقناة الكبيرة
            try:
                await client.send_file(
                    BIG_CHANNEL, 
                    event.message.media, 
                    caption=final_caption,
                    parse_mode='md'
                )
                await status_msg.edit(f"✅ تم النشر في @{BIG_CHANNEL}")
            except Exception as e:
                await status_msg.edit(f"❌ خطأ: {e}")

async def main():
    await client.start(bot_token=bot_token)
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
