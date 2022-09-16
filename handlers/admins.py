from asyncio.queues import QueueEmpty
from config import que
from pyrogram import Client, filters
from pyrogram.types import Message
from cache.admins import set
from helpers.decorators import authorized_users_only, errors
from helpers.channelmusic import get_chat_id
from helpers.filters import command, other_filters
from callsmusic import callsmusic, queues
from pytgcalls.types.input_stream import InputAudioStream
from pytgcalls.types.input_stream import InputStream


ACTV_CALLS = []

@Client.on_message(command(["/pause", "تحديث", "/rukja"]) & other_filters)
@errors
@authorized_users_only
async def pause(_, message: Message):
    await message.delete()
    await callsmusic.pytgcalls.pause_stream(message.chat.id)
    await message.reply_text("**» ᴍᴜsɪᴄ ᴘʟᴀʏᴇʀ ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ...**".format( message.from_user.mention ), )


@Client.on_message(command(["resume"]) & other_filters)
@errors
@authorized_users_only
async def resume(_, message: Message):
    await message.delete()
    await callsmusic.pytgcalls.resume_stream(message.chat.id)
    await message.reply_text("**» ᴍᴜsɪᴄ ᴘʟᴀʏᴇʀ sᴜᴄᴄᴇsғᴜʟʟʏ ʀᴇsᴜᴍᴇᴅ...**".format( message.from_user.mention ), )


@Client.on_message(command(["/end", "ايقاف", "اسكت"]) & other_filters)
@errors
@authorized_users_only
async def stop(_, message: Message):
    try:
        callsmusic.queues.clear(message.chat.id)
    except QueueEmpty:
        pass

    await message.delete()
    await callsmusic.pytgcalls.leave_group_call(message.chat.id)
    await message.reply_text("🐰**»حاضر هسكت...**".format(
      message.from_user.mention ), )

@Client.on_message(command(["تخطي", "/next"]) & other_filters)
@errors
@authorized_users_only
async def skip(_, message: Message):
    await message.delete()
    global que
    chat_id = message.chat.id
    for x in callsmusic.pytgcalls.active_calls:
        ACTV_CALLS.append(int(x.chat_id))
    if int(chat_id) not in ACTV_CALLS:
        await message.reply_text("💎**» تم التخطي للمسار التالي...**")
    else:
        queues.task_done(chat_id)
        
        if queues.is_empty(chat_id):
            await callsmusic.pytgcalls.leave_group_call(chat_id)
        else:
            await callsmusic.pytgcalls.change_stream(
                chat_id, 
                InputStream(
                    InputAudioStream(
                        callsmusic.queues.get(chat_id)["file"],
                    ),
                ),
            )
    await message.reply_text("» ᴛʀᴀᴄᴋ sᴋɪᴘᴘᴇᴅ".format( message.from_user.mention ), )
