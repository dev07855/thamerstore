import os
import asyncio
import re
from telethon import TelegramClient, events

# بياناتك
api_id = 23882332
api_hash = '1d515ac7bf517374b9ba7c0d8d74b3fd'
bot_token = '8604013302:AAHAZytEsZdTxyBlzn3-DsQuKjxEoc6jSL0'

# يوزر قناة أحمد (تأكد إن حسابك الشخصي مشترك فيها)
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
            
            # تنظيف اسم ملفك (مثال: infltr)
            clean_name = "".join(re.findall(r'[a-zA-Z]', file_name.rsplit('.', 1)[0])).lower()
            # بحث مرن بأول 3 حروف
            search_query = clean_name[:3] 
            
            final_caption = f"📱 تطبيق: **{file_name}**{MY_RIGHTS}"
            
            try:
                # محاولة جلب آخر 800 رسالة من قناة أحمد
                async for message in client.iter_messages(SOURCE_CHANNEL, limit=800):
                    # دمج النص من الرسالة أو الكابشن تحت الصورة
                    full_text = (message.text or "") + (message.caption or "")
                    
                    if full_text:
                        # تنظيف نص أحمد من كل الرموز للمطابقة
                        clean_target = "".join(re.findall(r'[a-zA-Z]', full_text)).lower()
                        
                        # مطابقة ذكية
                        if search_query in clean_target:
                            # ✅ سحب الوصف كامل كما هو (عربي وانجليزي)
                            final_caption = full_text + MY_RIGHTS
                            await status_msg.edit(f"✅ كفو! لقيت الوصف الكامل.")
                            break
            except Exception as e:
                print(f"Error: {e}")
                await status_msg.edit(f"⚠️ تنبيه: تأكد أن حسابك مشترك في قناة أحمد ديف.")

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
                await status_msg.edit(f"❌ خطأ في الإرسال: {e}")

async def main():
    await client.start(bot_token=bot_token)
    print("🚀 بوت THAMERDEV جاهز للانطلاق...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
