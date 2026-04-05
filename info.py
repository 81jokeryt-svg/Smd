import re
from os import environ
from Script import script 

id_pattern = re.compile(r'^.\d+$')

# Bot information
SESSION = environ.get('SESSION', 'Media_search')
API_ID = int(environ.get('API_ID', '13415474'))
API_HASH = environ.get('API_HASH', '01bb828c0429beeabd6e9e841d026231')
BOT_TOKEN = environ.get('BOT_TOKEN', "")

# This Pictures Is For Start Message Picture, You Can Add Multiple By Giving One Space Between Each.
PICS = (environ.get('PICS', 'https://graph.org/file/47d57543609f1faddbc6a.jpg https://graph.org/file/fee3dafdacf11af114a59.jpg https://graph.org/file/6038dbae3bd8e5cb44897.jpg https://graph.org/file/f735645d19aabd6d25d17.jpg https://graph.org/file/5ce463e5a2edf56470bb6.jpg https://graph.org/file/e101e043cab0269091c9d.jpg https://graph.org/file/fc2aebe2ebfe6808660ad.jpg https://graph.org/file/93254e40bd10e6fbeae5c.jpg https://graph.org/file/28c43ebc4de422f24b182.jpg https://graph.org/file/8f8cbdf63f0eeb235cc3f.jpg https://graph.org/file/9dbdb9f86952c106f9131.jpg https://graph.org/file/c6ac894696d5157c80964.jpg https://graph.org/file/ed2fb77f665081e916abb.jpg https://graph.org/file/0362105a1347d200a9667.jpg https://graph.org/file/57e5850ec173cc1db68da.jpg https://graph.org/file/473226bc919bd7524069c.jpg https://graph.org/file/1f129ddabdc480c6906af.jpg https://graph.org/file/8e87d194c787909c9c276.jpg https://graph.org/file/9c8504c9e43ad2f818f14.jpg https://graph.org/file/13f8f4d4b920b1ebe8792.jpg https://graph.org/file/a9a1413dee9df96872335.jpg https://graph.org/file/8e8c8912fb6aaf95fe1c2.jpg https://graph.org/file/3bc305e2288b24fd7913d.jpg https://graph.org/file/01ead07a6a742e67fa6bb.jpg https://graph.org/file/6a2dcd1f53f5b52de571c.jpg https://graph.org/file/49b217f0c63f3102a818c.jpg https://graph.org/file/f56a4041c05970f9835e7.jpg https://graph.org/file/3816445f78627859a257c.jpg https://graph.org/file/36eab7c50c2fea1db9c8e.jpg https://graph.org/file/2a73975d17aa75d4037c6.jpg https://graph.org/file/09d93ed056ff26f36fb56.jpg https://graph.org/file/e31b9dea19a627ddb0bfb.jpg https://graph.org/file/e84ad342a34172dbd6a14.jpg https://graph.org/file/1a2c4fa5e06670f7fd185.jpg https://graph.org/file/90872db0d0c6d23da0e29.jpg https://graph.org/file/85e18f57931e0f9498a5a.jpg https://graph.org/file/cb074803c16510e6d1c14.jpg https://graph.org/file/979cc7a3e3aaf5e9b412b.jpg https://graph.org/file/660718b9e623791974493.jpg https://graph.org/file/ef0e2897ddf5c8df82058.jpg https://graph.org/file/d3b93745600f2730a637d.jpg https://graph.org/file/9a3813b0755d25ea63800.jpg https://graph.org/file/55753abeb28db5c7a593b.jpg https://graph.org/file/e11d1f86a5589bae87f26.jpg https://graph.org/file/2bc7aa67b8e1e93265a04.jpg https://graph.org/file/bcbb9e4409c27134cce6c.jpg https://graph.org/file/f857e90b2452888611930.jpg')).split()

# Admins & Users
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('ADMINS', '').split()] # For Multiple Id Use One Space Between Each.
auth_users = [int(user) if id_pattern.search(user) else user for user in environ.get('AUTH_USERS', '').split()]  # For Multiple Id Use One Space Between Each.
AUTH_USERS = (auth_users + ADMINS) if auth_users else []
LOG_CHANNEL = int(environ.get('LOG_CHANNEL', '-1003725961309')) # This Channel Is For When User Start Your Bot Then Bot Send That User Name And Id In This Log Channel, Same For Group Also.
CHANNELS = [int(ch) if id_pattern.search(ch) else ch for ch in environ.get('CHANNELS', '-1003813513961').split()]  # For Multiple Id Use One Space Between Each.
auth_channel = environ.get('AUTH_CHANNEL', '-1003062629837') # give your force subscribe channel id here else leave it blank
AUTH_CHANNEL = int(auth_channel) if auth_channel and id_pattern.search(auth_channel) else None # This Is Force Subscribe Channel, also known as Auth Channel 
INDEX_REQ_CHANNEL = int(environ.get('INDEX_REQ_CHANNEL', LOG_CHANNEL)) # This Channel Is For Index Request
reqst_channel = environ.get('REQST_CHANNEL', '') # This Channel Is For When User Request Any File Name With command or hashtag like - /request or #request
REQST_CHANNEL = int(reqst_channel) if reqst_channel and id_pattern.search(reqst_channel) else None 
support_chat_id = environ.get('SUPPORT_CHAT_ID', '-1003219334269') # This Is Your Bot Support Group Id , Here Bot Will Not Give File Because This Is Support Group.
SUPPORT_CHAT_ID = int(support_chat_id) if support_chat_id and id_pattern.search(support_chat_id) else None
DELETE_CHANNELS = [int(dch) if id_pattern.search(dch) else dch for dch in environ.get('DELETE_CHANNELS', '-1003522165861').split()]  # For Multiple Id Use One Space Between Each.# This Channel Is For Delete Index File, Forward Your File In This Channel Which You Want To Delete Then Bot Automatically Delete That File From Database.

# if REQUEST_TO_JOIN_MODE is true then force subscribe work like request to join fsub, else if false then work like normal fsub.
REQUEST_TO_JOIN_MODE = bool(environ.get('REQUEST_TO_JOIN_MODE', False)) # Set True Or False
TRY_AGAIN_BTN = bool(environ.get('TRY_AGAIN_BTN', False)) # Set True Or False (This try again button is only for request to join fsub not for normal fsub)

# MongoDB information
DATABASE_URI = environ.get('DATABASE_URI', "mongodb+srv://urlmongodb:AAZWxt6Fbw3G2MZR@cluster0.kolo6q0.mongodb.net/?retryWrites=true&w=majority")# IF Multiple Database Is False Then Fill Only This Database Url.
DATABASE_NAME = environ.get('DATABASE_NAME', "cluster0xx")
COLLECTION_NAME = environ.get('COLLECTION_NAME', 'Telegram_F')

#Modes Calls and True & False
# Premium And Referal Settings
PREMIUM_AND_REFERAL_MODE = bool(environ.get('PREMIUM_AND_REFERAL_MODE', True)) # Set Ture Or False
# Rename Info : If True Then Bot Rename File Else Not
RENAME_MODE = bool(environ.get('RENAME_MODE', False)) # Set True or False
# Auto Approve Info : If True Then Bot Approve New Upcoming Join Request Else Not
AUTO_APPROVE_MODE = bool(environ.get('AUTO_APPROVE_MODE', False)) # Set True or False
#No need To Bool Multi database 
MULTIPLE_DATABASE = bool(environ.get('MULTIPLE_DATABASE', False)) # Set True or False

# If PREMIUM_AND_REFERAL_MODE is True Then Fill Below Variable, If Flase Then No Need To Fill.
REFERAL_COUNT = int(environ.get('REFERAL_COUNT', '20')) # number of referal count
REFERAL_PREMEIUM_TIME = environ.get('REFERAL_PREMEIUM_TIME', '1month') # time in week, day, month.
PAYMENT_QR = environ.get('PAYMENT_QR', 'https://graph.org/file/e538e5c45b510beb3e88b.jpg') # payment code picture url. can you create the same format
PAYMENT_TEXT = environ.get('PAYMENT_TEXT', '<b>- ᴀᴠᴀɪʟᴀʙʟᴇ ᴘʟᴀɴs - \n\n- 30ʀs - 1 ᴡᴇᴇᴋ\n- 50ʀs - 1 ᴍᴏɴᴛʜs\n- 120ʀs - 3 ᴍᴏɴᴛʜs\n- 220ʀs - 6 ᴍᴏɴᴛʜs\n\n🎁 ᴘʀᴇᴍɪᴜᴍ ғᴇᴀᴛᴜʀᴇs 🎁\n\n○ ɴᴏ ɴᴇᴇᴅ ᴛᴏ ᴠᴇʀɪғʏ\n○ ɴᴏ ɴᴇᴇᴅ ᴛᴏ ᴏᴘᴇɴ ʟɪɴᴋ\n○ ᴅɪʀᴇᴄᴛ ғɪʟᴇs\n○ ᴀᴅ-ғʀᴇᴇ ᴇxᴘᴇʀɪᴇɴᴄᴇ\n○ ʜɪɢʜ-sᴘᴇᴇᴅ ᴅᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋ\n○ ᴍᴜʟᴛɪ-ᴘʟᴀʏᴇʀ sᴛʀᴇᴀᴍɪɴɢ ʟɪɴᴋs\n○ ᴜɴʟɪᴍɪᴛᴇᴅ ᴍᴏᴠɪᴇs & sᴇʀɪᴇs\n○ ꜰᴜʟʟ ᴀᴅᴍɪɴ sᴜᴘᴘᴏʀᴛ\n○ ʀᴇǫᴜᴇsᴛ ᴡɪʟʟ ʙᴇ ᴄᴏᴍᴘʟᴇᴛᴇᴅ ɪɴ 1ʜ ɪꜰ ᴀᴠᴀɪʟᴀʙʟᴇ\n\n✨ ᴜᴘɪ ɪᴅ - <code>smdowner@ybl</code>\n\nᴄʟɪᴄᴋ ᴛᴏ ᴄʜᴇᴄᴋ ʏᴏᴜʀ ᴀᴄᴛɪᴠᴇ ᴘʟᴀɴ /myplan\n\n💢 ᴍᴜsᴛ sᴇɴᴅ sᴄʀᴇᴇɴsʜᴏᴛ ᴀғᴛᴇʀ ᴘᴀʏᴍᴇɴᴛ\n\n‼️ ᴀғᴛᴇʀ sᴇɴᴅɪɴɢ ᴀ sᴄʀᴇᴇɴsʜᴏᴛ ᴘʟᴇᴀsᴇ ɢɪᴠᴇ ᴜs sᴏᴍᴇ ᴛɪᴍᴇ ᴛᴏ ᴀᴅᴅ ʏᴏᴜ ɪɴ ᴛʜᴇ ᴘʀᴇᴍɪᴜᴍ</b>')

# Links
GRP_LNK = environ.get('GRP_LNK', 'https://t.me/SAM_DUB_LEEZZA')
CHNL_LNK = environ.get('CHNL_LNK', 'https://t.me/SAM_DUB_LEZHa')
SUPPORT_CHAT = environ.get('SUPPORT_CHAT', 'SMD_BOTz_Support') # Support Chat Link Without https://t.me or @
OWNER_LNK = environ.get('OWNER_LNK', 'SMD_Owner') # OWNER LNK Link Without https://t.me or @

# True Or False
AI_SPELL_CHECK = bool(environ.get('AI_SPELL_CHECK', True))
PM_SEARCH = bool(environ.get('PM_SEARCH', True))
BUTTON_MODE = bool(environ.get('BUTTON_MODE', True))
MAX_BTN = bool(environ.get('MAX_BTN', True))
IS_TUTORIAL = bool(environ.get('IS_TUTORIAL', False))
IMDB = bool(environ.get('IMDB', False))
AUTO_FFILTER = bool(environ.get('AUTO_FFILTER', True))
AUTO_DELETE = bool(environ.get('AUTO_DELETE', True))
LONG_IMDB_DESCRIPTION = bool(environ.get("LONG_IMDB_DESCRIPTION", False))
SPELL_CHECK_REPLY = bool(environ.get("SPELL_CHECK_REPLY", True))
MELCOW_NEW_USERS = bool(environ.get('MELCOW_NEW_USERS', False))
PROTECT_CONTENT = bool(environ.get('PROTECT_CONTENT', False))
PUBLIC_FILE_STORE = bool(environ.get('PUBLIC_FILE_STORE', True))
NO_RESULTS_MSG = bool(environ.get("NO_RESULTS_MSG", False))
USE_CAPTION_FILTER = bool(environ.get('USE_CAPTION_FILTER', True))

# Token Verification Info :
VERIFY = bool(environ.get('VERIFY', False))
VERIFY_SHORTLINK_URL = environ.get('VERIFY_SHORTLINK_URL', '')
VERIFY_SHORTLINK_API = environ.get('VERIFY_SHORTLINK_API', '')
VERIFY_TUTORIAL = environ.get('VERIFY_TUTORIAL', '')

# If You Fill Second Shortner Then Bot Attach Both First And Second Shortner And Use It For Verify.
VERIFY_SECOND_SHORTNER = bool(environ.get('VERIFY_SECOND_SHORTNER', False)) # if verify second shortner is True then fill below url and api
VERIFY_SND_SHORTLINK_URL = environ.get('VERIFY_SND_SHORTLINK_URL', '')
VERIFY_SND_SHORTLINK_API = environ.get('VERIFY_SND_SHORTLINK_API', '')

# Shortlink Info
SHORTLINK_MODE = bool(environ.get('SHORTLINK_MODE', False)) # Set True Or False
SHORTLINK_URL = environ.get('SHORTLINK_URL', '')
SHORTLINK_API = environ.get('SHORTLINK_API', '')
TUTORIAL = environ.get('TUTORIAL', '') # How Open Shortner Link Video Link , Channel Link Where You Upload Your Video.

# Others
DELETE_TIME = int(environ.get("DELETE_TIME", "300"))
CACHE_TIME = int(environ.get('CACHE_TIME', 1800))
MAX_B_TN = environ.get("MAX_B_TN", "5")
PORT = environ.get("PORT", "8080")
MSG_ALRT = environ.get('MSG_ALRT', '🍁sᴍᴅ-ʙᴏᴛᴢ🕊')
CUSTOM_FILE_CAPTION = environ.get("CUSTOM_FILE_CAPTION", f"{script.CAPTION}")
BATCH_FILE_CAPTION = environ.get("BATCH_FILE_CAPTION", CUSTOM_FILE_CAPTION)
IMDB_TEMPLATE = environ.get("IMDB_TEMPLATE", f"{script.IMDB_TEMPLATE_TXT}")
MAX_LIST_ELM = environ.get("MAX_LIST_ELM", None)


# Choose Option Settings 
LANGUAGES = ["malayalam", "mal", "tamil", "tam" ,"english", "eng", "hindi", "hin", "telugu", "tel", "kannada", "kan"]
SEASONS = ["season 1", "season 2", "season 3", "season 4", "season 5", "season 6", "season 7", "season 8", "season 9", "season 10"]
EPISODES = ["E01", "E02", "E03", "E04", "E05", "E06", "E07", "E08", "E09", "E10", "E11", "E12", "E13", "E14", "E15", "E16", "E17", "E18", "E19", "E20", "E21", "E22", "E23", "E24", "E25", "E26", "E27", "E28", "E29", "E30", "E31", "E32", "E33", "E34", "E35", "E36", "E37", "E38", "E39", "E40"]
QUALITIES = ["360p", "480p", "720p", "1080p", "1440p", "2160p"]
YEARS = ["1900", "1991", "1992", "1993", "1994", "1995", "1996", "1997", "1998", "1999", "2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025"]

# Online Stream and Download
STREAM_MODE = bool(environ.get('STREAM_MODE', False)) # Set True or False

# If Stream Mode Is True Then Fill All Required Variable, If False Then Don't Fill.
MULTI_CLIENT = False
SLEEP_THRESHOLD = int(environ.get('SLEEP_THRESHOLD', '60'))
PING_INTERVAL = int(environ.get("PING_INTERVAL", "1200"))  # 20 minutes
if 'DYNO' in environ:
    ON_HEROKU = True
else:
    ON_HEROKU = False
URL = environ.get("URL", "https://smdfilterxbot.koyeb.app/")

# Start Command Reactions
REACTIONS = ["🦋", "😇", "🤗", "😍", "👍", "🎅", "😐", "🥰", "🤩", "😱", "🤣", "😘", "👏", "😛", "😈", "🎉", "⚡️", "🫡", "🤓", "😎", "🏆", "🔥", "🤭", "🌚", "🆒", "👻", "😁"] #don't add any emoji because tg not support all emoji reactions

# If Multiple Database Is True Then Fill All Three Below Database Uri Else You Will Get Error.
O_DB_URI = environ.get('O_DB_URI', "")   # This Db Is For Other Data Store
F_DB_URI = environ.get('F_DB_URI', "")   # This Db Is For File Data Store
S_DB_URI = environ.get('S_DB_URI', "")   # This Db is for File Data Store When First Db Is Going To Be Full.


if MULTIPLE_DATABASE == False:
    USER_DB_URI = DATABASE_URI
    OTHER_DB_URI = DATABASE_URI
    FILE_DB_URI = DATABASE_URI
    SEC_FILE_DB_URI = DATABASE_URI
else:
    USER_DB_URI = DATABASE_URI    # This Db is for User Data Store
    OTHER_DB_URI = O_DB_URI       # This Db Is For Other Data Store
    FILE_DB_URI = F_DB_URI        # This Db Is For File Data Store
    SEC_FILE_DB_URI = S_DB_URI    # This Db is for File Data Store When First Db Is Going To Be Full.
