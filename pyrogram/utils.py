#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

import asyncio
import base64
import functools
import hashlib
import os
import re
import struct
from concurrent.futures.thread import ThreadPoolExecutor
from datetime import datetime, timezone
from getpass import getpass
from typing import Union, List, Dict, Optional

import pyrogram
from pyrogram import raw, enums
from pyrogram import types
from pyrogram.file_id import FileId, FileType, PHOTO_TYPES, DOCUMENT_TYPES


async def ainput(prompt: str = "", *, hide: bool = False):
    """Just like the built-in input, but async"""
    with ThreadPoolExecutor(1) as executor:
        func = functools.partial(getpass if hide else input, prompt)
        return await asyncio.get_event_loop().run_in_executor(executor, func)


def get_input_media_from_file_id(
    file_id: str,
    expected_file_type: FileType = None,
    ttl_seconds: int = None,
    has_spoiler: bool = None
) -> Union["raw.types.InputMediaPhoto", "raw.types.InputMediaDocument"]:
    try:
        decoded = FileId.decode(file_id)
    except Exception:
        raise ValueError(
            f'Failed to decode "{file_id}". The value does not represent an existing local file, '
            f"HTTP URL, or valid file id."
        )

    file_type = decoded.file_type

    if expected_file_type is not None and file_type != expected_file_type:
        raise ValueError(f"Expected {expected_file_type.name}, got {file_type.name} file id instead")

    if file_type in (FileType.THUMBNAIL, FileType.CHAT_PHOTO):
        raise ValueError(f"This file id can only be used for download: {file_id}")

    if file_type in PHOTO_TYPES:
        return raw.types.InputMediaPhoto(
            id=raw.types.InputPhoto(
                id=decoded.media_id,
                access_hash=decoded.access_hash,
                file_reference=decoded.file_reference
            ),
            ttl_seconds=ttl_seconds,
            spoiler=has_spoiler
        )

    if file_type in DOCUMENT_TYPES:
        return raw.types.InputMediaDocument(
            id=raw.types.InputDocument(
                id=decoded.media_id,
                access_hash=decoded.access_hash,
                file_reference=decoded.file_reference
            ),
            ttl_seconds=ttl_seconds,
            spoiler=has_spoiler
        )

    raise ValueError(f"Unknown file id: {file_id}")


async def parse_messages(
    client,
    messages: "raw.types.messages.Messages",
    is_scheduled: bool = False,
    replies: int = 1,
    business_connection_id: str = "",
    r: "raw.base.Updates" = None
) -> List["types.Message"]:
    parsed_messages = []

    if not messages and r:
        users = {i.id: i for i in getattr(r, "users", [])}
        chats = {i.id: i for i in getattr(r, "chats", [])}

        for u in getattr(r, "updates", []):
            if isinstance(
                u,
                (
                    raw.types.UpdateNewMessage,
                    raw.types.UpdateNewChannelMessage,
                    raw.types.UpdateNewScheduledMessage,
                )
            ):
                parsed_messages.append(
                    await types.Message._parse(
                        client,
                        u.message,
                        users,
                        chats,
                        is_scheduled=isinstance(u, raw.types.UpdateNewScheduledMessage),
                        replies=0
                    )
                )

            elif isinstance(
                u,
                (
                    raw.types.UpdateBotNewBusinessMessage,
                )
            ):
                parsed_messages.append(
                    await types.Message._parse(
                        client,
                        u.message,
                        users,
                        chats,
                        business_connection_id=getattr(u, "connection_id", business_connection_id),
                        raw_reply_to_message=u.reply_to_message
                    )
                )

        return types.List(parsed_messages)

    users = {i.id: i for i in messages.users}
    chats = {i.id: i for i in messages.chats}

    if not messages.messages:
        return types.List()

    for message in messages.messages:
        parsed_messages.append(
            await types.Message._parse(
                client,
                message,
                users,
                chats,
                is_scheduled=is_scheduled,
                replies=replies
            )
        )

    if replies and False:  # TODO
        messages_with_replies = {
            # TODO: fix this logic someday
            i.id: i.reply_to.reply_to_msg_id
            for i in messages.messages
            if not isinstance(i, raw.types.MessageEmpty) and i.reply_to
        }

        if messages_with_replies:
            # We need a chat id, but some messages might be empty (no chat attribute available)
            # Scan until we find a message with a chat available (there must be one, because we are fetching replies)
            for m in parsed_messages:
                if m.chat:
                    chat_id = m.chat.id
                    break
            else:
                chat_id = 0

            reply_messages = await client.get_messages(
                chat_id=chat_id,
                reply_to_message_ids=messages_with_replies.keys(),
                replies=replies - 1
            )

            for message in parsed_messages:
                reply_id = messages_with_replies.get(message.id, None)

                for reply in reply_messages:
                    if reply.id == reply_id:
                        message.reply_to_message = reply

    return types.List(parsed_messages)


def pack_inline_message_id(msg_id: "raw.base.InputBotInlineMessageID"):
    if isinstance(msg_id, raw.types.InputBotInlineMessageID):
        inline_message_id_packed = struct.pack(
            "<iqq",
            msg_id.dc_id,
            msg_id.id,
            msg_id.access_hash
        )
    else:
        inline_message_id_packed = struct.pack(
            "<iqiq",
            msg_id.dc_id,
            msg_id.owner_id,
            msg_id.id,
            msg_id.access_hash
        )

    return base64.urlsafe_b64encode(inline_message_id_packed).decode().rstrip("=")


def unpack_inline_message_id(inline_message_id: str) -> "raw.base.InputBotInlineMessageID":
    padded = inline_message_id + "=" * (-len(inline_message_id) % 4)
    decoded = base64.urlsafe_b64decode(padded)

    if len(decoded) == 20:
        unpacked = struct.unpack("<iqq", decoded)

        return raw.types.InputBotInlineMessageID(
            dc_id=unpacked[0],
            id=unpacked[1],
            access_hash=unpacked[2]
        )
    else:
        unpacked = struct.unpack("<iqiq", decoded)

        return raw.types.InputBotInlineMessageID64(
            dc_id=unpacked[0],
            owner_id=unpacked[1],
            id=unpacked[2],
            access_hash=unpacked[3]
        )


MIN_CHANNEL_ID = -1002147483647
MAX_CHANNEL_ID = -1000000000000
MIN_CHAT_ID_OLD = -2147483647
MIN_CHAT_ID = -999999999999
MAX_USER_ID_OLD = 2147483647
MAX_USER_ID = 999999999999


def get_raw_peer_id(peer: raw.base.Peer) -> Optional[int]:
    """Get the raw peer id from a Peer object"""
    if isinstance(peer, raw.types.PeerUser):
        return peer.user_id

    if isinstance(peer, raw.types.PeerChat):
        return peer.chat_id

    if isinstance(peer, raw.types.PeerChannel):
        return peer.channel_id

    return None


def get_peer_id(peer: raw.base.Peer) -> int:
    """Get the non-raw peer id from a Peer object"""
    if isinstance(peer, raw.types.PeerUser):
        return peer.user_id

    if isinstance(peer, raw.types.PeerChat):
        return -peer.chat_id

    if isinstance(peer, raw.types.PeerChannel):
        return MAX_CHANNEL_ID - peer.channel_id

    raise ValueError(f"Peer type invalid: {peer}")


def get_peer_type(peer_id: int) -> str:
    if peer_id < 0:
        if MIN_CHAT_ID <= peer_id:
            return "chat"

        if MIN_CHANNEL_ID <= peer_id < MAX_CHANNEL_ID:
            return "channel"
    elif 0 < peer_id <= MAX_USER_ID:
        return "user"

    raise ValueError(f"Peer id invalid: {peer_id}")


def get_channel_id(peer_id: int) -> int:
    return MAX_CHANNEL_ID - peer_id


def btoi(b: bytes) -> int:
    return int.from_bytes(b, "big")


def itob(i: int) -> bytes:
    return i.to_bytes(256, "big")


def sha256(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


def xor(a: bytes, b: bytes) -> bytes:
    return bytes(i ^ j for i, j in zip(a, b))


def compute_password_hash(
    algo: raw.types.PasswordKdfAlgoSHA256SHA256PBKDF2HMACSHA512iter100000SHA256ModPow,
    password: str
) -> bytes:
    hash1 = sha256(algo.salt1 + password.encode() + algo.salt1)
    hash2 = sha256(algo.salt2 + hash1 + algo.salt2)
    hash3 = hashlib.pbkdf2_hmac("sha512", hash2, algo.salt1, 100000)

    return sha256(algo.salt2 + hash3 + algo.salt2)


# noinspection PyPep8Naming
def compute_password_check(
    r: raw.types.account.Password,
    password: str
) -> raw.types.InputCheckPasswordSRP:
    algo = r.current_algo

    p_bytes = algo.p
    p = btoi(algo.p)

    g_bytes = itob(algo.g)
    g = algo.g

    B_bytes = r.srp_B
    B = btoi(B_bytes)

    srp_id = r.srp_id

    x_bytes = compute_password_hash(algo, password)
    x = btoi(x_bytes)

    g_x = pow(g, x, p)

    k_bytes = sha256(p_bytes + g_bytes)
    k = btoi(k_bytes)

    kg_x = (k * g_x) % p

    while True:
        a_bytes = os.urandom(256)
        a = btoi(a_bytes)

        A = pow(g, a, p)
        A_bytes = itob(A)

        u = btoi(sha256(A_bytes + B_bytes))

        if u > 0:
            break

    g_b = (B - kg_x) % p

    ux = u * x
    a_ux = a + ux
    S = pow(g_b, a_ux, p)
    S_bytes = itob(S)

    K_bytes = sha256(S_bytes)

    M1_bytes = sha256(
        xor(sha256(p_bytes), sha256(g_bytes))
        + sha256(algo.salt1)
        + sha256(algo.salt2)
        + A_bytes
        + B_bytes
        + K_bytes
    )

    return raw.types.InputCheckPasswordSRP(srp_id=srp_id, A=A_bytes, M1=M1_bytes)


async def parse_text_entities(
    client: "pyrogram.Client",
    text: str,
    parse_mode: Optional[enums.ParseMode],
    entities: List["types.MessageEntity"]
) -> Dict[str, Union[str, List[raw.base.MessageEntity]]]:
    if entities:
        # Inject the client instance because parsing user mentions requires it
        for entity in entities:
            entity._client = client

        text, entities = text, [await entity.write() for entity in entities] or None
    else:
        text, entities = (await client.parser.parse(text, parse_mode)).values()

    return {
        "message": text,
        "entities": entities
    }


async def parse_deleted_messages(client, update, users, chats) -> List["types.Message"]:
    messages = update.messages
    channel_id = getattr(update, "channel_id", None)
    business_connection_id = getattr(update, "connection_id", None)
    raw_business_peer = getattr(update, "peer", None)

    delete_chat = None
    if channel_id is not None:
        chan_id = get_channel_id(channel_id)
        # try:
        # TODO
        #     delete_chat = await client.get_chat(chan_id, False)
        # except pyrogram.errors.RPCError:
        delete_chat = types.Chat(
            id=chan_id,
            type=enums.ChatType.CHANNEL,
            client=client
        )

    elif raw_business_peer is not None:
        chat_id = get_raw_peer_id(raw_business_peer)
        # yet another TODO comment here
        if chat_id:
            if isinstance(raw_business_peer, raw.types.PeerUser):
                delete_chat = types.Chat._parse_user_chat(client, users[chat_id])

            elif isinstance(raw_business_peer, raw.types.PeerChat):
                delete_chat = types.Chat._parse_chat_chat(client, chats[chat_id])

            else:
                delete_chat = types.Chat._parse_channel_chat(
                    client, chats[chat_id]
                )

    parsed_messages = []

    for message in messages:
        parsed_messages.append(
            types.Message(
                id=message,
                chat=delete_chat,
                business_connection_id=business_connection_id,
                client=client
            )
        )

    return types.List(parsed_messages)


def zero_datetime() -> datetime:
    return datetime.fromtimestamp(0, timezone.utc)


def timestamp_to_datetime(ts: Optional[int]) -> Optional[datetime]:
    return datetime.fromtimestamp(ts) if ts else None


def datetime_to_timestamp(dt: Optional[datetime]) -> Optional[int]:
    return int(dt.timestamp()) if dt else None


async def _get_reply_message_parameters(
    client: "pyroram.Client",
    message_thread_id: int = None,
    reply_parameters: "types.ReplyParameters" = None
) -> Union[
    raw.types.InputReplyToStory,
    raw.types.InputReplyToMessage
]:
    reply_to = None
    if not reply_parameters:
        if message_thread_id:
            reply_to = raw.types.InputReplyToMessage(
                reply_to_msg_id=message_thread_id,
                top_msg_id=message_thread_id
            )
        return reply_to
    if (
       reply_parameters and
       reply_parameters.story_id and
       reply_parameters.chat_id
    ):
        return raw.types.InputReplyToStory(
            peer=await client.resolve_peer(reply_parameters.chat_id),
            story_id=reply_parameters.story_id
        )
    reply_to_message_id = reply_parameters.message_id
    if not reply_to_message_id:
        return reply_to
    reply_to = raw.types.InputReplyToMessage(
        reply_to_msg_id=reply_to_message_id
    )
    if message_thread_id:
        reply_to.top_msg_id = message_thread_id
    # TODO
    quote = reply_parameters.quote
    if quote is not None:
        quote_parse_mode = reply_parameters.quote_parse_mode
        quote_entities = reply_parameters.quote_entities
        message, entities = (await parse_text_entities(
            client,
            quote,
            quote_parse_mode,
            quote_entities
        )).values()
        reply_to.quote_text = message
        reply_to.quote_entities = entities
    if reply_parameters.chat_id:
        reply_to.reply_to_peer_id = await client.resolve_peer(reply_parameters.chat_id)
    if reply_parameters.quote_position:
        reply_to.quote_offset = reply_parameters.quote_position
    return reply_to


def is_plain_domain(url):
    # https://github.com/tdlib/td/blob/d963044/td/telegram/MessageEntity.cpp#L1778
    return (
        url.find('/') >= len(url) and
        url.find('?') >= len(url) and
        url.find('#') >= len(url)
    )


def get_first_url(message: "raw.types.Message") -> str:
    text = message.message
    entities = message.entities
    # duplicate code copied from parser.
    text = re.sub(r"^\s*(<[\w<>=\s\"]*>)\s*", r"\1", text)
    text = re.sub(r"\s*(</[\w</>]*>)\s*$", r"\1", text)
    SMP_RE = re.compile(r"[\U00010000-\U0010FFFF]")
    text_ = SMP_RE.sub(
        lambda match:  # Split SMP in two surrogates
        "".join(
            chr(i) for i in struct.unpack(
                "<HH", match.group().encode("utf-16le")
            )
        ),
        text
    )
    url = None
    for entity in entities:
        if isinstance(entity, raw.types.MessageEntityTextUrl):
            url = entity.url
            if len(url) <= 4:
                url = None
                continue
            else:
                break
        elif isinstance(entity, raw.types.MessageEntityUrl):
            url = text_[entity.offset:entity.offset+entity.length+1]
            if len(url) <= 4:
                url = None
                continue
            else:
                break
    text = text_.encode("utf-16", "surrogatepass").decode("utf-16")
    if url:
        if (
            url.startswith((
                "ton:", "tg:", "ftp:"
            )) or
            is_plain_domain(url)
        ):
            return None
        return url
    return None


def fix_up_voice_audio_uri(
    client: "pyroram.Client",
    file_name: str,
    dinxe: int
) -> str:
    un_posi_mt = [
        "application/zip",  # 0
        # https://t.me/c/1220993104/1360174
        "audio/mpeg",  # 1
        "audio/ogg",  # 2
    ]
    mime_type = client.guess_mime_type(file_name) or un_posi_mt[dinxe]
    # BEWARE: https://t.me/c/1279877202/31475
    if dinxe == 1 and mime_type == "audio/ogg":
        mime_type = "audio/opus"
    elif dinxe == 2 and mime_type == "audio/mpeg":
        mime_type = "audio/ogg"
    # BEWARE: https://t.me/c/1279877202/74
    return mime_type
