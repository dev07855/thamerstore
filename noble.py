import os
import zipfile
import asyncio
from telethon import TelegramClient, events

# بياناتك الصحيحة
api_id = 23882332
api_hash = '1d515ac7bf517374b9ba7c0d8d74b3fd'
bot_token = '8604013302:AAHAZytEsZdTxyBlzn3-DsQuKjxEoc6jSL0'

# القنوات
SOURCE_CHANNEL = 'A7maad_dev'  # القناة اللي بيسحب منها الوصف
BIG_CHANNEL = 'hvh32'          # قناتك الكبيرة

client = TelegramClient('noble_session', api_id, api_hash)

@client.on(events.NewMessage)
async def handler(event):
    if event.is_private and event.document:
        file_name = event.document.attributes[0].file_name if event.document.attributes else "app.ipa"
        if file_name.endswith('.ipa'):
            print(f"📦 استلمت تطبيق: {file_name}.. جاري البحث عن وصف...")
            search_query = file_name.rsplit('.', 1)[0]
            final_caption = f"📱 تطبيق: {search_query}\n\n(لم يتم العثور على وصف في المصدر)"
            try:
                async for message in client.iter_messages(SOURCE_CHANNEL, limit=50):
                    if message.text and (search_query.split('_')[0].lower() in message.text.lower()):
                        final_caption = message.text
                        print("✅ كفو! لقيت الوصف.")
                        break
            except Exception as e:
                print(f"⚠️ خطأ في المصدر: {e}")

            path = await event.download_media()
            thumb_path = "thumb.png"
            found_thumb = False
            try:
                with zipfile.ZipFile(path, 'r') as zip_ref:
                    icons = [f for f in zip_ref.namelist() if 'AppIcon' in f and f.endswith('.png')]
                    if icons:
                        with open(thumb_path, "wb") as f: f.write(zip_ref.read(icons[-1]))
                        found_thumb = True
            except: pass

            await client.send_file(BIG_CHANNEL, path, caption=final_caption, thumb=thumb_path if found_thumb else None)
            print(f"🚀 تم النشر بنجاح!")
            if os.path.exists(path): os.remove(path)
            if os.path.exists(thumb_path): os.remove(thumb_path)

async def main():
    await client.start(bot_token=bot_token)
    print("🚀 البوت جاهز يا ثامر! أرسل لي أي ملف IPA في الخاص الحين...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
