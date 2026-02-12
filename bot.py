import asyncio
import os
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile, CallbackQuery
from config import BOT_TOKEN
import keyboards as kb
import utils

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

bot = Bot(
    token=BOT_TOKEN,
    timeout=60
)
# ================= START =================
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        f"Salom {message.from_user.first_name}! 👋\n\n"
        "🔗 Link yuboring yoki musiqa topish uchun video/audio tashlang."
    )


# ================= LINK HANDLER =================
@dp.message(F.text.regexp(r'(https?://[^\s]+)'))
async def handle_links(message: types.Message):
    url = message.text.strip()

    # ❌ Instagram Stories bloklash
    if "instagram.com/stories" in url:
        await message.reply("❌ Instagram Stories yuklab bo'lmaydi.")
        return

    # ================= YOUTUBE =================
    if "youtube.com" in url or "youtu.be" in url:
        info = await asyncio.get_event_loop().run_in_executor(
            None, utils.get_video_info, url
        )

        if info:
            text = (
                f"🎬 Video ma'lumotlari:\n\n"
                f"📝 Nomi: {info['title']}\n"
                f"📦 Hajmi: {info['size_mb']} MB\n\n"
                f"Sifatni tanlang:"
            )
            await message.reply(text, reply_markup=kb.format_selector())
        else:
            await message.reply("❌ Video ma'lumotini olib bo'lmadi.")
        return

    # ================= INSTAGRAM / TIKTOK =================
    if any(x in url for x in ["instagram.com", "tiktok.com"]):

        status = await message.reply("⏳ Yuklanmoqda...")

        try:
            file_path = await asyncio.get_event_loop().run_in_executor(
                None, utils.download_social_video, url
            )

            if file_path and os.path.exists(file_path):

                await status.edit_text("📤 Yuborilmoqda...")

                await message.answer_video(
                    FSInputFile(file_path),
                    caption="🎬 Video yuklandi!\n\n🚀 One Tool tomonidan yuklandi\n@OneTool_bot"
                )

                await status.delete()

                # 🗑 Tozalash
                try:
                    os.remove(file_path)
                except:
                    pass

            else:
                await status.edit_text("❌ Yuklab bo'lmadi. (Login yoki link xato)")

        except Exception as e:
            await status.edit_text("❌ Xatolik yuz berdi.")
            print("SOCIAL ERROR:", e)


# ================= YOUTUBE DOWNLOAD =================
@dp.callback_query(F.data.startswith("dl_"))
async def process_download(callback: CallbackQuery):
    quality = callback.data.split("_")[1]
    url = callback.message.reply_to_message.text

    status = await callback.message.edit_text(f"⏳ Yuklanmoqda ({quality})...")

    try:
        file_path = await asyncio.get_event_loop().run_in_executor(
            None,
            utils.download_video,
            url,
            quality
        )

        if file_path and os.path.exists(file_path):

            await status.edit_text("📤 Yuborilmoqda...")

            file = FSInputFile(file_path)

            if quality == "audio":
                await callback.message.answer_audio(
                    file,
                    caption="🎵 One Tool orqali yuklandi 🚀\n@OneTool_bot"
                )
            else:
                await callback.message.answer_video(
                    file,
                    caption="🎬 Video yuklandi!\n\n🚀 One Tool tomonidan yuklandi\n@OneTool_bot"
                )

            await status.delete()

            # 🗑 Tozalash
            try:
                os.remove(file_path)
            except:
                pass

        else:
            await status.edit_text("❌ Yuklab bo'lmadi.")

    except Exception as e:
        await status.edit_text("❌ Xatolik yuz berdi.")
        print("YOUTUBE ERROR:", e)


# ================= SHAZAM =================
@dp.message(F.voice | F.audio | F.video | F.video_note)
async def handle_shazam_media(message: types.Message):

    status = await message.reply("🔍 Musiqa qidirilmoqda...")

    media = message.voice or message.audio or message.video or message.video_note
    file = await bot.get_file(media.file_id)

    if not os.path.exists("downloads"):
        os.makedirs("downloads")

    file_path = f"downloads/{media.file_id}.mp3"
    await bot.download_file(file.file_path, file_path)

    track = await utils.identify_track(file_path)

    # 🗑 Asl faylni o'chirish
    try:
        os.remove(file_path)
    except:
        pass

    if track:
        caption = f"✅ Topildi!\n\n🎵 {track['title']}\n👤 {track['author']}"
        await status.edit_text("🎵 Musiqa yuklanmoqda...")

        try:
            audio_path = await asyncio.get_event_loop().run_in_executor(
                None,
                utils.download_audio_by_title,
                f"{track['author']} - {track['title']}"
            )

            if audio_path and os.path.exists(audio_path):
                await message.answer_audio(
                    FSInputFile(audio_path),
                    caption=caption
                )

                # 🗑 Tozalash
                try:
                    os.remove(audio_path)
                except:
                    pass

                await status.delete()

            else:
                await status.edit_text("❌ Musiqa yuklab bo'lmadi.")

        except Exception as e:
            await status.edit_text("❌ Musiqa yuklashda xatolik.")
            print("SHAZAM ERROR:", e)

    else:
        await status.edit_text("❌ Musiqa topilmadi.")


# ================= MAIN =================
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
