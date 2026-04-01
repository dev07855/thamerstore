import os
import asyncio
import re
from telethon import TelegramClient, events
from telethon.tl.types import DocumentAttributeFilename

# بياناتك
api_id = 23882332
api_hash = '1d515ac7bf517374b9ba7c0d8d74b3fd'
bot_token = '8604013302:AAHAZytEsZdTxyBlzn3-DsQuKjxEoc6jSL0'

SOURCE_ID = -1002266265804  # القناة المصدر
BIG_CHANNEL = 'hvh32'        # قناتك
MY_RIGHTS = "\n\n━━━━━━━━━━━━━━━\n✨ تم النشر بواسطة: **THAMERDEV**"

client = TelegramClient('noble_session', api_id, api_hash)

@client.on(events.NewMessage)
async def handler(event):
    if not event.document:
        return

    # استخراج اسم الملف بشكل صحيح
    file_name = None
    for attr in event.document.attributes:
        if isinstance(attr, DocumentAttributeFilename):
            file_name = attr.file_name
            break

    if not file_name:
        return

    if not file_name.lower().endswith('.ipa'):
        return

    # رسالة انتظار
    status_msg = await event.reply(f"⏳ جاري البحث في القناة عن: **{file_name}**")

    # تنظيف الاسم
    clean_name = re.sub(r'([a-z])([A-Z])', r'\1 \2', file_name.rsplit('.', 1)[0])
    clean_name = re.sub(r'[^a-zA-Z0-9]', ' ', clean_name).lower()
    keywords = [w for w in clean_name.split() if len(w) > 2]

    final_caption = f"📱 تطبيق: **{file_name}**{MY_RIGHTS}"
    found = False

    try:
        # 🔥 البحث السريع باستخدام search
        search_query = " ".join(keywords)

        messages = await client.get_messages(
            SOURCE_ID,
            search=search_query,
            limit=10
        )

        for message in messages:
            text_content = message.text or ""

            if text_content:
                match_count = 0
                for word in keywords:
                    if word in text_content.lower():
                        match_count += 1

                # لازم كلمتين على الأقل
                if match_count >= 2:
                    final_caption = text_content + MY_RIGHTS
                    found = True
                    break

    except Exception as e:
        print(f"Search Error: {e}")

    # النشر
    try:
        await client.send_file(
            BIG_CHANNEL,
            event.message.media,
            caption=final_caption,
            parse_mode='md'
        )

        if found:
            await status_msg.edit("✅ تم النشر مع الوصف بنجاح")
        else:
            await status_msg.edit("⚠️ ما حصلت وصف مطابق، تم النشر بدون وصف")

    except Exception as e:
        await status_msg.edit(f"❌ خطأ: {e}")


async def main():
    await client.start(bot_token=bot_token)
    print("🚀 البوت شغال...")
    await client.run_until_disconnected()


if __name__ == '__main__':
    asyncio.run(main())
