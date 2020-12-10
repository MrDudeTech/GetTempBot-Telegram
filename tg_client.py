from io import BytesIO
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.types import InputPeerChannel
import threading
from config import *

def start() -> None:
    client = TelegramClient('tg_client', CLIENT_API_ID, CLIENT_API_HASH)
    client.start(bot_token=API_TOKEN)


def get_file_stream(message_ids):
    peer = InputPeerChannel(CHANNEL_REPLY_TELETHON_ID,
                            CHANNEL_REPLY_TELETHON_HASH)
    messages = []
    for message_id in message_ids:
        messages.append(client.get_message_history(
            peer, offset_id=message_id + 1, limit=1)[1][0])

    for message in messages:
        stream = BytesIO()
        thread = threading.Thread(target=client.download_media, args=(
            message,), kwargs={'file': stream})
        thread.daemon = True
        thread.start()
        pos = 0
        while (thread.is_alive()):
            stream.seek(pos)
            r = stream.read()
            pos += len(r)
            yield r
