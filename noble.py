import os
import zipfile
import asyncio
from telethon import TelegramClient, events

# بياناتك الصحيحة من my.telegram.org
api_id = 23882332
api_hash = '1d515ac7bf517374b9ba7c0d8d74b3fd'
bot_token = '8604013302:AAHAZytEsZdTxyBlzn3-DsQuKjxEoc6jSL0'

# القنوات
SOURCE_CHANNEL = 'A7maad_dev'  # قناة المصدر للوصف
BIG_CHANNEL = 'hvh32'          # قناتك الكبيرة للنشر

# إنشاء العميل باستخدام ملف السشن اللي رفعته
client = TelegramClient('noble_session', api_id, api_hash)

# الفلتر الجديد: يراقب الرسائل اللي توصل للبوت أو ترسلها لنفسك (Saved Messages)
@client.on(events.NewMessage)
async def handler(event):
    # التأكد أن الرسالة تحتوي على ملف
    if event.document:
        file_name = event.document.attributes[0].file_name if event.document.attributes else "app.ipa"
        
        # يشتغل فقط إذا كان الملف IPA
        if file_name.lower().endswith('.ipa'):
            print(f"📦 تم رصد ملف IPA: {file_name}")
            
            # تنظيف اسم الملف للبحث عن الوصف
            search_query = file_name.rsplit('.', 1)[0].split('_')[0].split('-')[0]
            final_caption = f"📱 تطبيق: {file_name}\n\n(لم يتم العثور على وصف في قناة المصدر)"
            
            print(f"🔍 جاري البحث عن وصف لـ '{search_query}' في @{SOURCE_CHANNEL}...")
            
            try:
                # البحث في آخر 100 رسالة في قناة أحمد ديف
                async for message in client.iter_messages(SOURCE_CHANNEL, limit=100):
                    if message.text and (search_query.lower() in message.text.lower()):
                        final_caption = message.text
                        print("✅ تم العثور على الوصف المناسب!")
                        break
            except Exception as e:
                print(f"⚠️ خطأ أثناء البحث عن الوصف: {e}")

            # تحميل الملف للسيرفر
            print(f"📥 جاري تحميل {file_name}...")
            path = await event.download_media()
            
            # محاولة استخراج الأيقونة
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

            # النشر في القناة الكبيرة
            print(f"📤 جاري الرفع إلى @{BIG_CHANNEL}...")
            await client.send_file(
                BIG_CHANNEL, 
                path, 
                caption=final_caption, 
                thumb=thumb_path if found_thumb else None
            )
            print(f"🚀 تم النشر بنجاح في {BIG_CHANNEL}!")
            
            # تنظيف الذاكرة
            if os.path.exists(path): os.remove(path)
            if os.path.exists(thumb_path): os.remove(thumb_path)

async def main():
    # تشغيل الحساب باستخدام السشن والتوكن
    await client.start(bot_token=bot_token)
    print("🚀 البوت شغال الآن يا ثامر.. جرب أرسل IPA للبوت أو للرسائل المحفوظة.")
    await client.run_until_disconnected()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
