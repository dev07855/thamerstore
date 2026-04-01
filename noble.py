import os
import zipfile
from telethon import TelegramClient, events

# بياناتك الخاصة من تليجرام
api_id = 23882332
api_hash = '1d515ac7bf517374b9ba740d8d74b3fd'
# التوكن حقك من BotFather
bot_token = '8604013302:AAHAZytEsZdTxyBlzn3-DsQuKjxEoc6jSL0'

# قنواتك يا ثامر
SOURCE_CHANNEL = 'A7maad_dev'  # القناة اللي يجيب منها الوصف والملف
BIG_CHANNEL = 'hvh32'          # قناتك الكبيرة (الهدف)

client = TelegramClient('noble_session', api_id, api_hash).start(bot_token=bot_token)

@client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def handler(event):
    # إذا الرسالة فيها ملف IPA أو ملف داتا
    if event.document:
        file_name = event.document.attributes[0].file_name if event.document.attributes else "file.ipa"
        print(f"🔎 جاري سحب تطبيق جديد: {file_name}")
        
        # تحميل الملف والوصف الأصلي
        caption = event.message.message
        path = await event.download_media()
        
        # محاولة ذكية لسحب أيقونة التطبيق (عشان المنشور يطلع فخم)
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
        except: pass

        # إرسال الملف لقناتك hvh32 مع الوصف والأيقونة
        await client.send_file(
            BIG_CHANNEL, 
            path, 
            caption=caption, 
            thumb=thumb_path if found_thumb else None
        )
        print(f"✅ تم نقل {file_name} بنجاح إلى قناتك الكبيرة")
        
        # تنظيف السيرفر
        if os.path.exists(path): os.remove(path)
        if os.path.exists(thumb_path): os.remove(thumb_path)

print("🚀 بوت نوبل ستار شغال الحين ويراقب القنوات...")
client.run_until_disconnected()
