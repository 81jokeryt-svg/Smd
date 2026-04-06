# Don't Remove Credit @VJ_Bots
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01

import logging, re, asyncio
from utils import temp
from info import ADMINS
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait, MessageNotModified
from pyrogram.errors.exceptions.bad_request_400 import ChannelInvalid, ChatAdminRequired, UsernameInvalid, UsernameNotModified
from info import INDEX_REQ_CHANNEL as LOG_CHANNEL
from database.ia_filterdb import save_file
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
lock = asyncio.Lock()

# --- 1. Callback Query Handler (Buttons Logic) ---
@Client.on_callback_query(filters.regex(r'^index'))
async def index_files_callback(bot, query):
    if query.data.startswith('index_cancel'):
        temp.CANCEL = True
        return await query.answer("Cancelling Indexing...", show_alert=True)
    
    # Data Parsing: index#status#chat#msg_id#user_id
    try:
        data = query.data.split("#")
        status = data[1]
        chat = data[2]
        lst_msg_id = data[3]
        from_user = data[4]
    except (IndexError, ValueError):
        return await query.answer("Invalid Data Format!", show_alert=True)

    if status == 'reject':
        await query.message.delete()
        await bot.send_message(
            int(from_user),
            f'❌ Your Submission for indexing `{chat}` has been declined by moderators.',
            reply_to_message_id=int(lst_msg_id)
        )
        return await query.answer("Request Rejected")

    if status == 'accept':
        if lock.locked():
            return await query.answer('Wait! Another process is running.', show_alert=True)
        
        await query.answer('Starting Indexing... 🚀', show_alert=True)
        msg = query.message

        if int(from_user) not in ADMINS:
            await bot.send_message(
                int(from_user),
                f'✅ Your Submission for `{chat}` has been accepted. Indexing started.',
                reply_to_message_id=int(lst_msg_id)
            )

        await msg.edit(
            "**Indexing in Progress...**",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton('🛑 Stop Indexing', callback_data='index_cancel')]]
            )
        )
        
        # Chat ID handle (Numeric ya Username)
        target_chat = int(chat) if str(chat).lstrip('-').isdigit() else chat
        await index_files_to_db(int(lst_msg_id), target_chat, msg, bot)

# --- 2. Index Command (Ask Feature) ---
@Client.on_message(filters.private & filters.command('index'))
async def send_for_index(bot, message):
    if message.from_user.id not in ADMINS:
        return await message.reply("Only Admins can use this command.")

    try:
        # Kurigram ask feature (Requires Pyromod)
        vj = await bot.ask(
            chat_id=message.chat.id, 
            text="**📤 Send me the last message link or forward the last message from the channel.**",
            timeout=60
        )
    except Exception:
        return await message.reply("❌ **Timeout!** Command cancelled. Try again /index")

    if vj.forward_from_chat and vj.forward_from_chat.type == enums.ChatType.CHANNEL:
        last_msg_id = vj.forward_from_message_id
        chat_id = vj.forward_from_chat.username or vj.forward_from_chat.id
    elif vj.text:
        regex = re.compile("(https://)?(t\.me/|telegram\.me/|telegram\.dog/)(c/)?(\d+|[a-zA-Z_0-9]+)/(\d+)$")
        match = regex.match(vj.text)
        if not match:
            return await vj.reply('**Invalid Link!** Try again /index')
        chat_id = match.group(4)
        last_msg_id = int(match.group(5))
        if chat_id.isnumeric():
            chat_id = int(("-100" + chat_id))
    else:
        return await vj.reply("Unsupported input. Send Link or Forward Message.")

    # Channel Admin Check & Verification
    try:
        await bot.get_chat(chat_id)
        k = await bot.get_messages(chat_id, last_msg_id)
        if k.empty:
            raise Exception("Message not found.")
    except Exception as e:
        return await message.reply(f"**Error:** Make sure I'm Admin in the channel.\n`{e}`")

    # Confirmation Buttons
    buttons = [
        [InlineKeyboardButton('✅ Start Indexing', callback_data=f'index#accept#{chat_id}#{last_msg_id}#{message.from_user.id}')],
        [InlineKeyboardButton('❌ Cancel', callback_data='close_data')]
    ]
    
    await message.reply(
        f"**Target Chat:** `{chat_id}`\n**Last Message ID:** `{last_msg_id}`\n\nDo you want to start indexing this channel?",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# --- 3. Set Skip Number ---
@Client.on_message(filters.command('setskip') & filters.user(ADMINS))
async def set_skip_number(bot, message):
    try:
        skip = int(message.text.split(" ", 1)[1])
        temp.CURRENT = skip
        await message.reply(f"✅ Skip number set to: `{skip}`")
    except:
        await message.reply("Usage: `/setskip 100`")

# --- 4. Indexing Core Logic (The Most Important Part) ---
async def index_files_to_db(lst_msg_id, chat, msg, bot):
    total_files = 0
    duplicate = 0
    errors = 0
    deleted = 0
    no_media = 0
    unsupported = 0
    
    async with lock:
        try:
            temp.CANCEL = False
            current = temp.CURRENT
            
            # Kurigram get_chat_history is more stable for long tasks
            async for message in bot.get_chat_history(chat, limit=lst_msg_id, offset_id=temp.CURRENT):
                if temp.CANCEL:
                    break
                
                current += 1
                # Har 30 message baad progress update karein
                if current % 30 == 0:
                    try:
                        await msg.edit_text(
                            text=f"Total Processed: `{current}`\nSaved: `{total_files}`\nDuplicates: `{duplicate}`\nDeleted: `{deleted}`",
                            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('🛑 Stop', callback_data='index_cancel')]])
                        )
                    except MessageNotModified: 
                        pass

                if message.empty:
                    deleted += 1
                    continue
                elif not message.media:
                    no_media += 1
                    continue
                elif message.media not in [enums.MessageMediaType.VIDEO, enums.MessageMediaType.DOCUMENT, enums.MessageMediaType.AUDIO]:
                    unsupported += 1
                    continue
                
                media = getattr(message, message.media.value, None)
                if not media: 
                    unsupported += 1
                    continue
                
                media.caption = message.caption
                # Database mein save karna
                is_saved, status = await save_file(media)
                
                if is_saved: 
                    total_files += 1
                elif status == 0: 
                    duplicate += 1
                elif status == 2: 
                    errors += 1
                    
        except Exception as e:
            logger.exception(e)
            await msg.edit(f"**Indexing Stopped due to Error:**\n`{e}`")
        else:
            await msg.edit(
                f"✅ **Indexing Successfully Completed!**\n\n"
                f"📂 Total Saved: `{total_files}`\n"
                f"⏩ Duplicates: `{duplicate}`\n"
                f"❌ Errors: `{errors}`\n"
                f"🗑️ Deleted/Empty: `{deleted}`\n"
                f"🚫 Non-Media: `{no_media + unsupported}`"
            
