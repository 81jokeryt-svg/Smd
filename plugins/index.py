import logging, re, asyncio
from utils import temp
from info import ADMINS
# 'emoji' hata diya gaya hai taaki crash na ho
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait, MessageNotModified
from pyrogram.errors.exceptions.bad_request_400 import ChannelInvalid, ChatAdminRequired, UsernameInvalid, UsernameNotModified
from info import INDEX_REQ_CHANNEL as LOG_CHANNEL
from database.ia_filterdb import save_file
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
lock = asyncio.Lock()

@Client.on_callback_query(filters.regex(r'^index'))
async def index_files(bot, query):
    if query.data.startswith('index_cancel'):
        temp.CANCEL = True
        return await query.answer("Indexing Cancel ho rahi hai...", show_alert=True)
    
    # Safe split to avoid "not enough values to unpack"
    data = query.data.split("#")
    if len(data) < 5:
        return await query.answer("Invalid Callback Data!", show_alert=True)
        
    _, raju, chat, lst_msg_id, from_user = data
    
    if raju == 'reject':
        await query.message.delete()
        await bot.send_message(
            int(from_user),
            f'Aapki indexing request ({chat}) moderators ne reject kar di hai.',
            reply_to_message_id=int(lst_msg_id)
        )
        return

    if lock.locked():
        return await query.answer('Purani process khatam hone ka intezar karein.', show_alert=True)
    
    msg = query.message
    await query.answer('Processing Shuru... ⏳', show_alert=True)
    
    if int(from_user) not in ADMINS:
        await bot.send_message(
            int(from_user),
            f'Aapki request accept ho gayi hai aur files jald hi add ho jayengi.',
            reply_to_message_id=int(lst_msg_id)
        )
        
    await msg.edit(
        "**Indexing Shuru Ho Rahi Hai...**",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton('STOP / CANCEL', callback_data='index_cancel')]]
        )
    )
    
    try:
        chat = int(chat)
    except:
        pass # Username hai toh string hi rehne do
        
    await index_files_to_db(int(lst_msg_id), chat, msg, bot)

@Client.on_message(filters.private & filters.command('index'))
async def send_for_index(bot, message):
    # Kurigram/v2 enums usage
    vj = await bot.ask(message.chat.id, "**Channel ka link bhejiye ya last post forward kijiye.**")
    
    if vj.forward_from_chat and vj.forward_from_chat.type == enums.ChatType.CHANNEL:
        last_msg_id = vj.forward_from_message_id
        chat_id = vj.forward_from_chat.id
    elif vj.text:
        regex = re.compile(r"(https://)?(t\.me/|telegram\.me/|telegram\.dog/)(c/)?(\d+|[a-zA-Z_0-9]+)/(\d+)$")
        match = regex.match(vj.text)
        if not match:
            return await vj.reply('Link galat hai! Dubara /index try karein.')
        
        chat_id = match.group(4)
        last_msg_id = int(match.group(5))
        if chat_id.isnumeric():
            chat_id = int(("-100" + chat_id))
    else:
        return

    try:
        chat_info = await bot.get_chat(chat_id)
    except Exception as e:
        return await vj.reply(f'Error: {e}\n\nCheck karein ki bot channel mein Admin hai ya nahi.')

    if message.from_user.id in ADMINS:
        buttons = [[
            InlineKeyboardButton('YES, START', callback_data=f'index#accept#{chat_id}#{last_msg_id}#{message.from_user.id}')
        ]]
        return await message.reply(
            f'**Chat:** `{chat_info.title}`\n**ID:** `{chat_id}`\n\nKya aap ise index karna chahte hain?',
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    # For normal users
    await bot.send_message(
        LOG_CHANNEL,
        f'#IndexRequest\nBy: {message.from_user.mention}\nChat: `{chat_id}`',
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton('Accept ✅', callback_data=f'index#accept#{chat_id}#{last_msg_id}#{message.from_user.id}'),
            InlineKeyboardButton('Reject ❌', callback_data=f'index#reject#{chat_id}#{message.id}#{message.from_user.id}')
        ]])
    )
    await message.reply('Aapki request moderators ko bhej di gayi hai.')

async def index_files_to_db(lst_msg_id, chat, msg, bot):
    total_files, duplicate, errors, deleted, no_media, unsupported = 0, 0, 0, 0, 0, 0
    
    async with lock:
        try:
            current = temp.CURRENT
            temp.CANCEL = False
            
            # Kurigram supports get_chat_history for fast fetching
            async for message in bot.get_chat_history(chat, limit=lst_msg_id, offset=temp.CURRENT):
                if temp.CANCEL:
                    break
                
                current += 1
                if current % 50 == 0: # 50 messages ke baad update
                    try:
                        await msg.edit_text(
                            text=f"**Indexing Status:**\n\nFetched: `{current}`\nSaved: `{total_files}`\nSkipped: `{duplicate}`",
                            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('STOP', callback_data='index_cancel')]])
                        )
                    except MessageNotModified:
                        pass

                if not message or message.empty:
                    deleted += 1
                    continue
                if not message.media:
                    no_media += 1
                    continue
                
                # Filter media types using Kurigram enums
                if message.media not in [enums.MessageMediaType.VIDEO, enums.MessageMediaType.AUDIO, enums.MessageMediaType.DOCUMENT]:
                    unsupported += 1
                    continue

                media = getattr(message, message.media.value, None)
                if media:
                    media.caption = message.caption
                    # DB Save logic
                    is_saved, status = await save_file(media)
                    if is_saved:
                        total_files += 1
                    elif status == 0:
                        duplicate += 1
                    else:
                        errors += 1
                        
            await msg.edit(f"✅ **Indexing Complete!**\n\nTotal Saved: `{total_files}`\nDuplicates: `{duplicate}`\nErrors: `{errors}`")
            
        except Exception as e:
            logger.exception(e)
            await msg.edit(f"❌ **Fatal Error:** `{e}`")
