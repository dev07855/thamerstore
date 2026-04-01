import os
import zipfile
import asyncio
import re
from telethon import TelegramClient, events

# بياناتك
api_id = 23882332
api_hash = '1d515ac7bf517374b9ba7c0d8d74b3fd'
bot_token = '8604013302:AAHAZytEsZdTxyBlzn3-DsQuKjxEoc6jSL0'

SOURCE_CHANNEL = 'A7maad_dev'
BIG_CHANNEL = 'hvh32'

client = TelegramClient('noble_session', api_id, api_hash)

# دالة تحديث النسبة المئوية
async def progress_callback(current, total, msg, action):
    percentage = current * 100 / total
    if int(percentage) % 10 == 0:
        try:
            await msg.edit(f"⏳ **{action}...**\n\nالنسبة: `{percentage:.1f}%`\nالحجم: `{current / (1024 * 1024):.1f}MB` / `{total / (1024 * 1024):.1f}MB`")
        except:
            pass

@client.on(events.NewMessage)
async def handler(event):
    if event.document and event.document.attributes:
        file_name = event.document.attributes[0].file_name
        if file_name.lower().endswith('.ipa'):
            
            # 1. إشعار استلام الملف
            status_msg = await event.reply(f"🚀 استلمت: **{file_name}**\nجاري البدء...")
            
            # 2. تحميل الملف مع عداد
            path = await event.download_media(
                progress_callback=lambda c, t: progress_callback(c, t, status_msg, "جاري تحميل الملف من عندك")
            )
            
            # 3. إشعار جلب الوصف (اللي طلبته)
            await status_msg.edit(f"🔍 **جاري جلب الوصف من @{SOURCE_CHANNEL}...**\nيرجى الانتظار، جاري مطابقة البيانات.")
            
            clean_name = re.sub(r'[^a-zA-Z\s]', ' ', file_name.rsplit('.', 1)[0]).strip()
            search_query = ' '.join(clean_name.split()[:2]) 
            final_caption = f"📱 تطبيق: {file_name}\n\n(لم يتم العثور على وصف في المصدر)"
            
            try:
                found = False
                async for message in client.iter_messages(SOURCE_CHANNEL, limit=150):
                    if message.text:
                        if search_query.lower() in message.text.lower() or clean_name.split()[0].lower() in message.text.lower():
                            final_caption = message.text
                            found = True
                            break
                
                if found:
                    await status_msg.edit(f"✅ **تم جلب الوصف بنجاح!**\nجاري الآن استخراج الأيقونة والرفع...")
                else:
                    await status_msg.edit(f"⚠️ **لم يتم العثور على وصف مناسب.**\nسأقوم بنشره بالاسم فقط.")
            except:
                pass

            # 4. الأيقونة والرفع
            thumb_path = "thumb.png"
            found_thumb = False
            try:
                with zipfile.ZipFile(path, 'r') as zip_ref:
                    icons = [f for f in zip_ref.namelist() if 'AppIcon' in f and f.endswith('.png')]
                    if icons:
                        with open(thumb_path, "wb") as f: f.write(zip_ref.read(icons[-1]))
                        found_thumb = True
            except: pass

            # 5. عداد الرفع للقناة
            await client.send_file(
                BIG_CHANNEL, 
                path, 
                caption=final_caption, 
                thumb=thumb_path if found_thumb else None,
                progress_callback=lambda c, t: progress_callback(c, t, status_msg, "جاري الرفع لقناتك الكبيرة")
            )
            
            # 6. النهاية
            await status_msg.edit(f"✅ **تم النشر بنجاح يا ثامر!**\nالملف صار في قناة: @{BIG_CHANNEL}")
            
            if os.path.exists(path): os.remove(path)
            if os.path.exists(thumb_path): os.remove(thumb_path)

async def main():
    await client.start(bot_token=bot_token)
    print("🚀 بوت التحديثات شغال...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
