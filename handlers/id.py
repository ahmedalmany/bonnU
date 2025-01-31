from pyrogram import Client
from pyrogram.types import Message

from config import BOT_USERNAME
from helpers.filters import command
from helpers.get_file_id import get_file_id


@Client.on_message(command(["ايدي", "stickerid", "stkid", "stckrid", f"ايدي@{BOT_USERNAME}"]))
async def showid(_, message: Message):
    await message.delete()
    chat_type = message.chat.type

    if chat_type == "private":
        user_id = message.chat.id
        await message.reply_text(f"<code>{user_id}</code>")

    elif chat_type in ["group", "supergroup"]:
        _id = ""
        _id += "<b>ايدي الدردشة </b>: " f"<code>{message.chat.id}</code>\n"
        if message.reply_to_message:
            _id += (
                "<b>👍 ايدي بتاعك يا حلو</b>: "
                f"<code>{message.reply_to_message.from_user.id}</code>\n"
            )
            file_info = get_file_id(message.reply_to_message)
        else:
            _id += "<b>👍 ايدي بتاعك يا حلو </b>: " f"<code>{message.from_user.id}</code>\n"
            file_info = get_file_id(message)
        if file_info:
            _id += (
                f"<b>{file_info.message_type}</b>: "
                f"<code>{file_info.file_id}</code>\n"
            )
        await message.reply_text(_id)
