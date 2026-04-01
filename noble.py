import os
import asyncio
import re
from telethon import TelegramClient, events

# بياناتك
api_id = 23882332
api_hash = '1d515ac7bf517374b9ba7c0d8d74b3fd'
bot_token = '8604013302:AAHAZytEsZdTxyBlzn3-DsQuKjxEoc6jSL0'

# القنوات (تم تعديل الآيدي الرقمي بناءً على الصورة)
SOURCE_ID = -1002266265804  # أيدي قناة نوبل ستار تحديثات
BIG_CHANNEL = 'hvh32'        # القناة الكبيرة

# حقوقك
MY_RIGHTS = "\n\n━━━━━━━━━━━━━━━\n✨ تم النشر بواسطة: **THAMERDEV**"

client = TelegramClient('noble_session', api_id, api_hash)

@client.on(events.NewMessage)
async def handler(event):
    if event.document and event.document.attributes:
        file_name = event.document.attributes[0].file_name
        if file_name.lower().endswith('.ipa'):
            
            status_msg = await event.reply(f"🔍 جاري مطابقة ملف **{file_name}** مع تحديثات نوبل ستار...")
            
            # تنظيف اسم الملف وتقسيمه لكلمات للبحث المرن
            clean_name = re.sub(r'[^a-zA-Z0-9]', ' ', file_name.rsplit('.', 1)[0]).lower()
            keywords = [w for w in clean_name.split() if len(w) > 2]
            
            final_caption = f"📱 تطبيق: **{file_name}**{MY_RIGHTS}"
            found = False
            
            try:
                # البحث في القناة باستخدام الآيدي الرقمي (أضمن طريقة)
                async for message in client.iter_messages(SOURCE_ID, limit=800):
                    # سحب النص سواء كان رسالة أو كابشن تحت صورة التحديث
                    text_content = (message.text or "") + (message.caption or "")
                    
                    if text_content:
                        # إذا وجد أي كلمة من اسم الملف داخل نص التحديث
                        for word in keywords:
                            if word in text_content.lower():
                                final_caption = text_content + MY_RIGHTS
                                found = True
                                break
                    if found: break
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
                if found:
                    await status_msg.edit(f"✅ تم سحب وصف التحديث بنجاح من نوبل ستار!")
                else:
                    await status_msg.edit(f"⚠️ لم أجد إعلان تحديث مطابق، تم النشر بالاسم فقط.")
            except Exception as e:
                await status_msg.edit(f"❌ خطأ في النشر: {e}")

async def main():
    await client.start(bot_token=bot_token)
    print("🚀 بوت THAMERDEV يعمل الآن بنظام الآيدي الرقمي...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
