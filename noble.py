import os
import asyncio
import re
from telethon import TelegramClient, events

# بياناتك
api_id = 23882332
api_hash = '1d515ac7bf517374b9ba7c0d8d74b3fd'
bot_token = '8604013302:AAHAZytEsZdTxyBlzn3-DsQuKjxEoc6jSL0'

# القنوات
SOURCE_CHANNEL = 'NOPELSTAR'  # قناة إعلانات التحديث (صور ونصوص)
BIG_CHANNEL = 'hvh32'         # قناة نشر ملفات الـ IPA

# توقيعك الفخم
MY_RIGHTS = "\n\n━━━━━━━━━━━━━━━\n✨ تم النشر بواسطة: **THAMERDEV**"

client = TelegramClient('noble_session', api_id, api_hash)

@client.on(events.NewMessage)
async def handler(event):
    # البوت يشتغل لما ترسل له ملف IPA في الخاص
    if event.document and event.document.attributes:
        file_name = event.document.attributes[0].file_name
        if file_name.lower().endswith('.ipa'):
            
            status_msg = await event.reply(f"🔍 جاري مطابقة ملف **{file_name}** مع إعلانات التحديث في @{SOURCE_CHANNEL}...")
            
            # 1. استخراج كلمات البحث من اسم الملف (مثلاً: CityOfDragons -> city, dragons)
            clean_name = re.sub(r'([a-z])([A-Z])', r'\1 \2', file_name.rsplit('.', 1)[0])
            clean_name = re.sub(r'[^a-zA-Z0-9]', ' ', clean_name).lower()
            keywords = [w for w in clean_name.split() if len(w) > 2]
            
            # الوصف الافتراضي إذا ما لقى إعلان
            final_caption = f"📱 تطبيق: **{file_name}**{MY_RIGHTS}"
            found = False
            
            try:
                # 2. البحث في منشورات (الصور والنصوص) في نوبل ستار
                async for message in client.iter_messages(SOURCE_CHANNEL, limit=600):
                    # سحب النص من المنشور (سواء كان نص عادي أو نص تحت صورة)
                    full_text = (message.text or "") + (message.caption or "")
                    
                    if full_text:
                        # المطابقة: نبحث عن كلمات اسم الملف داخل إعلان التحديث
                        match_count = 0
                        for word in keywords:
                            if word in full_text.lower():
                                match_count += 1
                        
                        # إذا لقى كلمة أو أكثر (مثلاً لقى "Dragons" في بوستر التحديث)
                        if match_count >= 1:
                            # ✅ يسحب وصف التحديث كامل (العربي والانجليزي)
                            final_caption = full_text + MY_RIGHTS
                            found = True
                            break
            except Exception as e:
                print(f"Error: {e}")

            if found:
                await status_msg.edit(f"✅ تم العثور على إعلان التحديث وسحب الوصف!")
            else:
                await status_msg.edit(f"⚠️ لم أجد إعلان تحديث لهذا التطبيق في نوبل ستار.")

            # 3. إرسال ملف الـ IPA للقناة الكبيرة بالوصف الجديد
            try:
                await client.send_file(
                    BIG_CHANNEL, 
                    event.message.media, 
                    caption=final_caption,
                    parse_mode='md'
                )
                await status_msg.edit(f"✅ تم النشر بنجاح في @{BIG_CHANNEL}")
            except Exception as e:
                await status_msg.edit(f"❌ خطأ أثناء النقل: {e}")

async def main():
    await client.start(bot_token=bot_token)
    print("🚀 بوت THAMERDEV جاهز لمطابقة التحديثات...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
