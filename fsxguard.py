from telethon import TelegramClient, events, Button
from telethon.tl.functions.channels import GetParticipantRequest, EditBannedRequest
from telethon.tl.types import ChannelParticipantAdmin, ChannelParticipantCreator, ChatBannedRights
import os
import random
import asyncio
import time

# Konfigurasi API
API_ID = 20600399
API_HASH = "982e2c08d2f731d0424271c2f88525ca"
BOT_TOKEN = "7869449304:AAFzNBalYADEvX3FeoLCXP70umMA6k9XAwU"

# Inisialisasi bot
client = TelegramClient("bot", API_ID, API_HASH).start(bot_token=BOT_TOKEN)
last_bot_message = None

# Daftar pengguna whitelist dan blacklist
WHITELIST_USERS = set()
BLACKLIST_USERS = set()

def save_list(filename, data):
    with open(filename, "w") as f:
        f.write("\n".join(map(str, data)))

def load_list(filename):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return set(map(int, f.read().splitlines()))
    return set()

WHITELIST_USERS = load_list("whitelist.txt")
BLACKLIST_USERS = load_list("blacklist.txt")

# Fungsi untuk mengecek apakah pengguna adalah admin
async def is_admin(event):
    chat = await event.get_chat()
    sender = await event.get_sender()
    try:
        participant = await client(GetParticipantRequest(chat.id, sender.id))
        return isinstance(participant.participant, (ChannelParticipantAdmin, ChannelParticipantCreator))
    except:
        return False

# Fungsi untuk menghapus pesan dari non-admin dan mute mereka
@client.on(events.NewMessage())
async def delete_non_admin(event):
    if event.is_private:
        return
    if event.text.startswith("/"):
        if not await is_admin(event):
            await event.delete()
            await client.edit_permissions(event.chat_id, event.sender_id, send_messages=False)

# Handler untuk /unmute
@client.on(events.NewMessage(pattern=r"^/unmute(?: (.+))?"))
async def unmute(event):
    if not await is_admin(event):
        return
    user = event.pattern_match.group(1)
    user_id = None
    
    if event.reply_to_msg_id:
        reply = await event.get_reply_message()
        user_id = reply.sender_id
    elif user:
        try:
            if user.isdigit():
                user_id = int(user)
            else:
                user_entity = await client.get_entity(user)
                user_id = user_entity.id
        except:
            msg = await event.reply("<blockquote>⚠️ ᴛɪᴅᴀᴋ ᴅᴀᴘᴀᴛ ᴍᴇɴᴇᴍᴜᴋᴀɴ ᴘᴇɴɢɢᴜɴᴀ.</blockquote>", parse_mode="html")
            await asyncio.sleep(10)
            await msg.delete()
            return
    
    if user_id:
        await client(EditBannedRequest(event.chat_id, user_id, ChatBannedRights(until_date=None, send_messages=False)))
        msg = await event.reply(f"<blockquote>✅ ᴘᴇɴɢɢᴜɴᴀ ᴛᴇʟᴀʜ ᴅɪ-ᴜɴᴍᴜᴛᴇ.</blockquote>", parse_mode="html")
        await asyncio.sleep(10)
        await msg.delete()

# Fungsi untuk mendapatkan ID pengguna dari username, ID langsung, atau balasan
async def get_user_id(event, identifier):
    if event.is_reply:
        reply_msg = await event.get_reply_message()
        return reply_msg.sender_id
    if identifier.isdigit():
        return int(identifier)
    try:
        user = await client.get_entity(identifier)
        return user.id
    except:
        return None

# Handler untuk /start
@client.on(events.NewMessage(pattern=r"^/start"))
async def start(event):
    buttons = [[Button.inline("ᴅᴀғᴛᴀʀ ᴘᴇʀɪɴᴛᴀʜ", b"help")]]
    await event.reply(f"""<blockquote><b>🤖 sᴇʟᴀᴍᴀᴛ ᴅᴀᴛᴀɴɢ ᴅɪ ғʀᴇᴇsᴇx ɢᴜᴀʀᴅɪᴀɴ ʙᴏᴛ</b></blockquote> 
<blockquote>sᴀʏᴀ ᴀᴅᴀʟᴀʜ sᴇʙᴜᴀʜ ʙᴏᴛ ᴀsɪsᴛᴇɴ ɢʀᴜᴘ ʏᴀɴɢ ʙɪsᴀ ᴍᴇɴᴊᴀɢᴀ ɢʀᴜᴘ ᴀɴᴅᴀ ᴛᴇᴛᴀᴘ ʙᴇʀsɪʜ</blockquote>

<blockquote>sɪʟᴀᴋᴀɴ ᴛᴀᴍʙᴀʜᴋᴀɴ sᴀʏᴀ ᴋᴇ ɢʀᴜᴘ ᴀɴᴅᴀ sᴇʙᴀɢᴀɪ ᴀᴅᴍɪɴ</blockquote>

<b>ᴛᴇᴋᴀɴ ᴛᴏᴍʙᴏʟ ᴅɪʙᴀᴡᴀʜ ᴜɴᴛᴜᴋ ᴍᴇʟɪʜᴀᴛ ᴅᴀғᴛᴀʀ ᴘᴇʀɪɴᴛᴀʜ 👇🏻<b>
    """, buttons=buttons, parse_mode="html")

@client.on(events.CallbackQuery(data=b"help"))
async def help_callback(event):
    await event.edit(f"""📜ᴅᴀғᴛᴀʀ ᴘᴇʀɪɴᴛᴀʜ ʙᴏᴛ :
<blockquote>/start - ᴍᴇᴍᴜʟᴀɪ ʙᴏᴛ</blockquote>

<blockquote>/ping - ᴍᴇɴɢᴇᴄᴇᴋ ʟᴀᴛᴇɴsɪ ʙᴏᴛ</blockquote>

<blockquote>/help - ᴜɴᴛᴜᴋ ᴍᴇʟɪʜᴀᴛ ᴅᴀғᴛᴀʀ ᴘᴇʀɪɴᴛᴀʜ ʙᴏᴛ</blockquote>

<blockquote>/addbl  ʙᴀʟᴀs ᴋᴇ ᴘᴇsᴀɴ ᴀᴛᴀᴜ @username - ᴜɴᴛᴜᴋ ᴍᴇɴᴀᴍʙᴀʜᴋᴀɴ ᴘᴇɴɢɢᴜɴᴀ ᴋᴇ ʙʟᴀᴄᴋʟɪsᴛ</blockquote>

<blockquote>/delbl ʙᴀʟᴀs ᴋᴇ ᴘᴇsᴀɴ ᴀᴛᴀᴜ @username - ᴜɴᴛᴜᴋ ᴍᴇɴɢʜᴀᴘᴜs ᴘᴇɴɢɢᴜɴᴀ ᴅᴀʀɪ ʙʟᴀᴄᴋʟɪsᴛ</blockquote>

<blockquote>/addwhite ʙᴀʟᴀs ᴋᴇ ᴘᴇsᴀɴ ᴀᴛᴀᴜ @username - ᴍᴇɴᴀᴍʙᴀʜᴋᴀɴ ᴘᴇɴɢɢᴜɴᴀ ᴋᴇ ᴡʜɪᴛᴇʟɪsᴛ</blockquote>

<blockquote>/delwhite ʙᴀʟᴀs ᴋᴇ ᴘᴇsᴀɴ ᴀᴛᴀᴜ @username -  ᴍᴇɴɢʜᴀᴘᴜs ᴘᴇɴɢɢᴜɴᴀ ᴅᴀʀɪ ᴡʜɪᴛᴇʟɪsᴛ</blockquote>

<blockquote>/tagall - ᴜɴᴛᴜᴋ ᴍᴇɴᴛɪᴏɴ sᴇᴍᴜᴀ ᴀɴɢɢᴏᴛᴀ ɢʀᴜᴘ</blockquote>

<blockquote>/stoptagall - ᴜɴᴛᴜᴋ ᴍᴇɴɢʜᴇɴᴛɪᴋᴀɴ ᴛᴀɢᴀʟʟ</blockquote>
""", parse_mode="html")

# Handler untuk /ping
@client.on(events.NewMessage(pattern=r"^/ping"))
async def ping(event):
    start_time = time.time()
    msg = await event.reply("<blockquote>🏓 ᴘᴏɴɢ! ᴍᴇɴɢʜɪᴛᴜɴɢ ʟᴀᴛᴇɴsɪ . . .</blockquote>", parse_mode="html")
    end_time = time.time()
    latency = round((end_time - start_time) * 1000)
    await msg.edit(f"<blockquote>🏓 ᴘᴏɴɢ! ʟᴀᴛᴇɴsɪ : {latency} ᴍs</blockquote>", parse_mode="html")

# Handler untuk /help
@client.on(events.NewMessage(pattern=r"^/help"))
async def help_command(event):
    help_text = """
<b>📜ᴅᴀғᴛᴀʀ ᴘᴇʀɪɴᴛᴀʜ ʙᴏᴛ :</b>
<blockquote>/start - ᴍᴇᴍᴜʟᴀɪ ʙᴏᴛ</blockquote>

<blockquote>/ping - ᴍᴇɴɢᴇᴄᴇᴋ ʟᴀᴛᴇɴsɪ ʙᴏᴛ</blockquote>

<blockquote>/help - ᴜɴᴛᴜᴋ ᴍᴇʟɪʜᴀᴛ ᴅᴀғᴛᴀʀ ᴘᴇʀɪɴᴛᴀʜ ʙᴏᴛ</blockquote>

<blockquote>/addbl  ʙᴀʟᴀs ᴋᴇ ᴘᴇsᴀɴ ᴀᴛᴀᴜ @username - ᴜɴᴛᴜᴋ ᴍᴇɴᴀᴍʙᴀʜᴋᴀɴ ᴘᴇɴɢɢᴜɴᴀ ᴋᴇ ʙʟᴀᴄᴋʟɪsᴛ</blockquote>

<blockquote>/delbl ʙᴀʟᴀs ᴋᴇ ᴘᴇsᴀɴ ᴀᴛᴀᴜ @username - ᴜɴᴛᴜᴋ ᴍᴇɴɢʜᴀᴘᴜs ᴘᴇɴɢɢᴜɴᴀ ᴅᴀʀɪ ʙʟᴀᴄᴋʟɪsᴛ</blockquote>

<blockquote>/addwhite ʙᴀʟᴀs ᴋᴇ ᴘᴇsᴀɴ ᴀᴛᴀᴜ @username - ᴍᴇɴᴀᴍʙᴀʜᴋᴀɴ ᴘᴇɴɢɢᴜɴᴀ ᴋᴇ ᴡʜɪᴛᴇʟɪsᴛ</blockquote>

<blockquote>/delwhite ʙᴀʟᴀs ᴋᴇ ᴘᴇsᴀɴ ᴀᴛᴀᴜ @username -  ᴍᴇɴɢʜᴀᴘᴜs ᴘᴇɴɢɢᴜɴᴀ ᴅᴀʀɪ ᴡʜɪᴛᴇʟɪsᴛ</blockquote>

<blockquote>/tagall - ᴜɴᴛᴜᴋ ᴍᴇɴᴛɪᴏɴ sᴇᴍᴜᴀ ᴀɴɢɢᴏᴛᴀ ɢʀᴜᴘ</blockquote>

<blockquote>/stoptagall - ᴜɴᴛᴜᴋ ᴍᴇɴɢʜᴇɴᴛɪᴋᴀɴ ᴛᴀɢᴀʟʟ</blockquote>
"""
    await event.reply(help_text, parse_mode="html")

# Hapus pesan bot sebelumnya jika ada pesan baru
@client.on(events.NewMessage(outgoing=True))
async def auto_delete_bot_messages(event):
    global last_bot_message
    if last_bot_message:
        try:
            await last_bot_message.delete()
        except:
            pass
    last_bot_message = event
    await asyncio.sleep(3)
    await event.delete()

# Handler untuk blacklist dan whitelist
@client.on(events.NewMessage(pattern=r"^/(addbl|delbl|addwhite|delwhite)(?:\s+(.+))?"))
async def manage_lists(event):
    if not await is_admin(event):
        return
    command, identifier = event.pattern_match.groups()
    user_id = await get_user_id(event, identifier) if identifier or event.is_reply else None
    if not user_id:
        await event.reply("<blockquote>❌ ᴘᴇɴɢɢᴜɴᴀ ᴛɪᴅᴀᴋ ᴅɪᴛᴇᴍᴜᴋᴀɴ!</blockquote>", parse_mode="html")
        return
    user = await client.get_entity(user_id)
    mention = f"<a href='tg://user?id={user.id}'>{user.first_name}</a>"
    if command == "addbl":
        BLACKLIST_USERS.add(user_id)
        save_list("blacklist.txt", BLACKLIST_USERS)
        msg = await event.reply(f"<blockquote>🚫 {mention} ᴅɪᴛᴀᴍʙᴀʜᴋᴀɴ ᴋᴇ ʙʟᴀᴄᴋʟɪsᴛ!</blockquote>", parse_mode="html")
    elif command == "delbl":
        BLACKLIST_USERS.discard(user_id)
        save_list("blacklist.txt", BLACKLIST_USERS)
        msg = await event.reply(f"<blockquote>✅ {mention} ᴅɪʜᴀᴘᴜs ᴅᴀʀɪ ʙʟᴀᴄᴋʟɪsᴛ!</blockquote>", parse_mode="html")
    elif command == "addwhite":
        WHITELIST_USERS.add(user_id)
        save_list("whitelist.txt", WHITELIST_USERS)
        msg = await event.reply(f"<blockquote>✅ {mention} ᴅɪᴛᴀᴍʙᴀʜᴋᴀɴ ᴋᴇ ᴡʜɪᴛᴇʟɪsᴛ!</blockquote>", parse_mode="html")
    elif command == "delwhite":
        WHITELIST_USERS.discard(user_id)
        save_list("whitelist.txt", WHITELIST_USERS)
        msg = await event.reply(f"<blockquote>✅ {mention} ᴅɪʜᴀᴘᴜs ᴅᴀʀɪ ᴡʜɪᴛᴇʟɪsᴛ!</blockquote>", parse_mode="html")
    await asyncio.sleep(10)
    await msg.delete()

# Handler untuk tagall
running_tagall = {}

@client.on(events.NewMessage(pattern=r"^/tagall(?: (.*))?"))
async def tagall(event):
    if not await is_admin(event):
        return
    chat = await event.get_chat()
    participants = await client.get_participants(chat)
    text = event.pattern_match.group(1) or "naik sini sayang"
    
    emojis = ["🔥", "⚡", "💥", "🎯", "🚀", "🎉"]
    mentions = []
    for user in participants:
        if user.bot:
            continue
        emoji = random.choice(emojis)
        mention = f'<a href="tg://user?id={user.id}">{emoji}</a>'
        mentions.append(mention)
    
    running_tagall[event.chat_id] = True
    chunk_size = 6
    
    for i in range(0, len(mentions), chunk_size):
        if not running_tagall.get(event.chat_id, False):
            break
        mention_text = " ".join(mentions[i:i+chunk_size])
        await client.send_message(event.chat_id, f"<blockquote>{text}</blockquote>\n\n<blockquote>{mention_text}</blockquote>\n\n<blockquote><b>Powered by @OfficialFreesex</b></blockquote>", parse_mode="html")
        await asyncio.sleep(3) #jeda agar tidak spam
    
    running_tagall[event.chat_id] = False
    await event.reply("<blockquote>✅ sᴇʟᴇsᴀɪ ᴍᴇɴᴛɪᴏɴ sᴇᴍᴜᴀ ᴀɴɢɢᴏᴛᴀ.</blockquote>", parse_mode="html")

@client.on(events.NewMessage(pattern=r"^/stoptagall"))
async def stoptagall(event):
    if not await is_admin(event):
        return
    running_tagall[event.chat_id] = False
    await event.reply("<blockquote>🛑 ᴛᴀɢᴀʟʟ ᴛᴇʟᴀʜ ᴅɪʜᴇɴᴛɪᴋᴀɴ.</blockquote>", parse_mode="html")

# Handler utama untuk mendeteksi pesan GCast
@client.on(events.NewMessage)
async def handler(event):
    global last_bot_message
    if event.is_private or not event.text:
        return
    sender = await event.get_sender()
    if sender.id in WHITELIST_USERS:
        return
    if sender.id in BLACKLIST_USERS:
        await event.delete()
        msg = await event.reply("<blockquote>🚫 ᴘᴇsᴀɴ ᴀɴᴅᴀ ᴅɪʜᴀᴘᴜs ᴋᴀʀᴇɴᴀ ᴊᴇʟᴇᴋ!</blockquote>", parse_mode="html")
        last_bot_message = msg
        await asyncio.sleep(3)
        await msg.delete()
        return

print("Guardian Freesex sedang bertugas...")
client.run_until_disconnected()
