import os
import asyncio
import re
from telethon import TelegramClient, events

# بياناتك
api_id = 23882332
api_hash = '1d515ac7bf517374b9ba7c0d8d74b3fd'
bot_token = '8604013302:AAHAZytEsZdTxyBlzn3-DsQuKjxEoc6jSL0'

SOURCE_ID = -1002266265804  # نوبل ستار
BIG_CHANNEL = 'hvh32'        # القناة الكبيرة
MY_RIGHTS = "\n\n━━━━━━━━━━━━━━━\n✨ تم النشر بواسطة: **THAMERDEV**"

client = TelegramClient('noble_session', api_id, api_hash)

@client.on(events.NewMessage)
async def handler(event):
    if event.document and event.document.attributes:
        file_name = event.document.attributes[0].file_name
        if file_name.lower().endswith('.ipa'):
            
            # رسالة تنبيه تفاعلية
            status_msg = await event.reply(f"⏳ جاري البحث العميق في أرشيف @NOPELSTAR... لـ **{file_name}**")
            
            # تنظيف الاسم (Life Sim 3D -> life, sim)
            clean_name = re.sub(r'([a-z])([A-Z])', r'\1 \2', file_name.rsplit('.', 1)[0])
            clean_name = re.sub(r'[^a-zA-Z0-9]', ' ', clean_name).lower()
            keywords = [w for w in clean_name.split() if len(w) > 2]
            
            final_caption = f"📱 تطبيق: **{file_name}**{MY_RIGHTS}"
            found = False
            
            try:
                # --- البحث المتعمق بنظام المجموعات ---
                offset_id = 0
                search_limit = 1000 # بنفحص آخر 1000 رسالة بدقة
                
                while offset_id < search_limit:
                    # جلب الرسائل 100 بـ 100 عشان ما "يهنق" البحث
                    messages = await client.get_messages(SOURCE_ID, limit=100, offset_id=offset_id)
                    if not messages:
                        break
                    
                    for message in messages:
                        text_content = (message.text or "") + (message.caption or "")
                        if text_content:
                            # فحص كل كلمة من اسم الملف داخل نص القناة
                            match_count = 0
                            for word in keywords:
                                if word in text_content.lower():
                                    match_count += 1
                            
                            # إذا لقى أي كلمة مطابقة (مثل Life أو Sim)
                            if match_count >= 1:
                                final_caption = text_content + MY_RIGHTS
                                found = True
                                break
                    
                    if found: break
                    offset_id += len(messages)
                    await asyncio.sleep(0.5) # راحة بسيطة للسيرفر عشان ما ينحظر
                            
            except Exception as e:
                print(f"Error in search: {e}")

            # النشر النهائي
            try:
                await client.send_file(BIG_CHANNEL, event.message.media, caption=final_caption, parse_mode='md')
                if found:
                    await status_msg.edit(f"✅ تم النشر بنجاح مع الوصف المستخرج!")
                else:
                    await status_msg.edit(f"⚠️ بحثت في آخر 1000 منشور ولم أجد وصفاً مطابقاً.")
            except Exception as e:
                await status_msg.edit(f"❌ خطأ: {e}")

async def main():
    await client.start(bot_token=bot_token)
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
