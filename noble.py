import os
import asyncio
import re
from telethon import TelegramClient, events

# بياناتك
api_id = 23882332
api_hash = '1d515ac7bf517374b9ba7c0d8d74b3fd'
bot_token = '8604013302:AAHAZytEsZdTxyBlzn3-DsQuKjxEoc6jSL0'

# القنوات
SOURCE_CHANNEL = 'NOPELSTAR'  # قناة إعلانات الصور والنصوص
BIG_CHANNEL = 'hvh32'         # قناة الـ IPA

# توقيعك
MY_RIGHTS = "\n\n━━━━━━━━━━━━━━━\n✨ تم النشر بواسطة: **THAMERDEV**"

client = TelegramClient('noble_session', api_id, api_hash)

@client.on(events.NewMessage)
async def handler(event):
    if event.document and event.document.attributes:
        file_name = event.document.attributes[0].file_name
        if file_name.lower().endswith('.ipa'):
            
            status_msg = await event.reply(f"⏳ جاري مطابقة إعلان التحديث لـ **{file_name}**...")
            
            # --- استخراج البصمة (مثلاً: CityOfDragons -> cityofdragons) ---
            # نشيل كل شي ونخلي بس الحروف الصغيرة
            clean_file = "".join(re.findall(r'[a-zA-Z]', file_name.rsplit('.', 1)[0])).lower()
            
            final_caption = f"📱 تطبيق: **{file_name}**{MY_RIGHTS}"
            found = False
            
            try:
                # مسح شامل لآخر 1000 منشور (عشان نضمن نلقاه)
                async for message in client.iter_messages(SOURCE_CHANNEL, limit=1000):
                    full_text = (message.text or "") + (message.caption or "")
                    
                    if full_text:
                        # تنظيف نص القناة (نشيل المسافات والرموز)
                        clean_target = "".join(re.findall(r'[a-zA-Z]', full_text)).lower()
                        
                        # مطابقة "البصمة": لو أول 4 حروف من ملفك موجودة في نص القناة
                        # أو لو اسم ملفك المنظف موجود داخل نص القناة المنظف
                        if clean_file[:4] in clean_target or clean_file in clean_target:
                            final_caption = full_text + MY_RIGHTS
                            found = True
                            break
            except Exception as e:
                print(f"Error: {e}")

            # النشر الفوري (بدون تحميل)
            try:
                await client.send_file(
                    BIG_CHANNEL, 
                    event.message.media, 
                    caption=final_caption,
                    parse_mode='md'
                )
                if found:
                    await status_msg.edit(f"✅ تم سحب الوصف من إعلان التحديث بنجاح!")
                else:
                    await status_msg.edit(f"⚠️ لم أجد إعلاناً مطابقاً.. تم النشر بالاسم فقط.")
            except Exception as e:
                await status_msg.edit(f"❌ خطأ: {e}")

async def main():
    await client.start(bot_token=bot_token)
    print("🚀 نظام THAMERDEV للمطابقة الشاملة شغال...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
