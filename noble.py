import os
import zipfile
import asyncio
from telethon import TelegramClient, events

# بياناتك الصحيحة يا ثامر
api_id = 23882332
api_hash = '1d515ac7bf517374b9ba7c0d8d74b3fd'
bot_token = '8604013302:AAHAZytEsZdTxyBlzn3-DsQuKjxEoc6jSL0'

# قنواتك
SOURCE_CHANNEL = 'A7maad_dev'  # المصدر
BIG_CHANNEL = 'hvh32'          # قناتك الكبيرة

client = TelegramClient('noble_session', api_id, api_hash)

@client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def handler(event):
    if event.document:
        file_name = event.document.attributes[0].file_name if event.document.attributes else "file.ipa"
        print(f"🔎 جاري سحب ملف: {file_name}")
        
        caption = event.message.message
        path = await event.download_media()
        
        thumb_path = "thumb.png"
        found_thumb = False
        try:
            if file_name.endswith('.ipa'):
                with zipfile.ZipFile(path, 'r') as zip_ref:
                    icons = [f for f in zip_ref.namelist() if 'AppIcon' in f and f.endswith('.png')]
                    if icons:
                        with open(thumb_path, "wb") as f:
                            f.write(zip_ref.read(icons[-1]))
                        found_thumb = True
        except:
            pass

        await client.send_file(
            BIG_CHANNEL, 
            path, 
            caption=caption, 
            thumb=thumb_path if found_thumb else None
        )
        print(f"✅ تم النقل بنجاح إلى قناتك {BIG_CHANNEL}")
        
        if os.path.exists(path): os.remove(path)
        if os.path.exists(thumb_path): os.remove(thumb_path)

async def main():
    # تشغيل البوت باستخدام التوكن
    await client.start(bot_token=bot_token)
    print("🚀 مبروك يا ثامر! البوت شغال الآن وبدون أي أخطاء...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
