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
MY_RIGHTS = "\n\n✨ تم النشر بواسطة: [نوبل ستار](https://t.me/hvh32)"

client = TelegramClient('noble_session', api_id, api_hash)

@client.on(events.NewMessage)
async def handler(event):
    if event.document and event.document.attributes:
        file_name = event.document.attributes[0].file_name
        if file_name.lower().endswith('.ipa'):
            
            status_msg = await event.reply(f"🚀 **جاري مطابقة البيانات...** لـ {file_name}")
            
            # استخراج الحروف فقط من اسم ملفك (مثال: royalmatch)
            clean_name = "".join(re.findall(r'[a-zA-Z]', file_name.rsplit('.', 1)[0])).lower()
            # نأخذ أول 5 حروف للبحث المرن
            search_query = clean_name[:5] 
            
            final_caption = f"📱 تطبيق: {file_name}{MY_RIGHTS}"
            
            try:
                # بحث عميق في آخر 400 رسالة
                async for message in client.iter_messages(SOURCE_CHANNEL, limit=400):
                    full_text = (message.text or "") + (message.caption or "")
                    if full_text:
                        # تنظيف نص رسالة أحمد من كل الرموز والشرطات (-)
                        # ونخليها بس حروف عشان التطابق يكون 100%
                        clean_target = "".join(re.findall(r'[a-zA-Z]', full_text)).lower()
                        
                        if search_query in clean_target:
                            final_caption = full_text + MY_RIGHTS
                            await status_msg.edit(f"✅ كفو! لقيت الوصف (تخطيت الرموز والشرطات)")
                            break
            except Exception as e:
                print(f"Error: {e}")

            # النقل الفوري السريع
            try:
                await client.send_file(BIG_CHANNEL, event.message.media, caption=final_caption, parse_mode='md')
                await status_msg.edit(f"✅ **تم النشر بنجاح!**")
            except Exception as e:
                await status_msg.edit(f"❌ خطأ في الإرسال: {e}")

async def main():
    await client.start(bot_token=bot_token)
    print("🚀 البوت شغال بنظام 'تجاهل الرموز'...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
