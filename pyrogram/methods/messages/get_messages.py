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

import logging
from typing import Union, List, Iterable

import pyrogram
from pyrogram import raw, types, utils
from pyrogram.types.messages_and_media.message import Str

log = logging.getLogger(__name__)


# TODO: Rewrite using a flag for replied messages and have message_ids non-optional


class GetMessages:
    async def get_messages(
        self: "pyrogram.Client",
        chat_id: Union[int, str] = None,
        message_ids: Union[int, Iterable[int]] = None,
        reply_to_message_ids: Union[int, Iterable[int]] = None,
        replies: int = 1,
        is_scheduled: bool = False,
        link: str = None,
    ) -> Union["types.Message", List["types.Message"]]:
        """Get one or more messages from a chat by using message identifiers.

        You can retrieve up to 200 messages at once.

        .. include:: /_includes/usable-by/users-bots.rst

        You must use exactly one of ``chat_id`` OR ``link``.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            message_ids (``int`` | Iterable of ``int``, *optional*):
                Pass a single message identifier or an iterable of message ids (as integers) to get the content of the
                message themselves.

            reply_to_message_ids (``int`` | Iterable of ``int``, *optional*):
                Pass a single message identifier or an iterable of message ids (as integers) to get the content of
                the previous message you replied to using this message.
                If *message_ids* is set, this argument will be ignored.

            replies (``int``, *optional*):
                The number of subsequent replies to get for each message.
                Pass 0 for no reply at all or -1 for unlimited replies.
                Defaults to 1.

            is_scheduled (``bool``, *optional*):
                Whether to get scheduled messages. Defaults to False.

            link (``str``):
                A link of the message, usually can be copied using ``Copy Link`` functionality OR obtained using :obj:`~pyrogram.raw.types.Message.link` OR  :obj:`~pyrogram.raw.functions.channels.ExportMessageLink`

        Returns:
            :obj:`~pyrogram.types.Message` | List of :obj:`~pyrogram.types.Message`: In case *message_ids* was not
            a list, a single message is returned, otherwise a list of messages is returned.

        Example:
            .. code-block:: python

                # Get one message
                await app.get_messages(chat_id=chat_id, message_ids=12345)

                # Get more than one message (list of messages)
                await app.get_messages(chat_id=chat_id, message_ids=[12345, 12346])

                # Get message by ignoring any replied-to message
                await app.get_messages(chat_id=chat_id, message_ids=message_id, replies=0)

                # Get message with all chained replied-to messages
                await app.get_messages(chat_id=chat_id, message_ids=message_id, replies=-1)

                # Get the replied-to message of a message
                await app.get_messages(chat_id=chat_id, reply_to_message_ids=message_id)

        Raises:
            ValueError: In case of invalid arguments.
        """
        if chat_id:
            ids, ids_type = (
                (message_ids, raw.types.InputMessageID) if message_ids
                else (reply_to_message_ids, raw.types.InputMessageReplyTo) if reply_to_message_ids
                else (None, None)
            )

            if ids is None:
                raise ValueError("No argument supplied. Either pass message_ids or reply_to_message_ids")

            peer = await self.resolve_peer(chat_id)

            is_iterable = not isinstance(ids, int)
            ids = list(ids) if is_iterable else [ids]

            if replies < 0:
                replies = (1 << 31) - 1

            if is_scheduled:
                rpc = raw.functions.messages.GetScheduledMessages(
                    peer=peer,
                    id=ids
                )
            else:
                ids = [ids_type(id=i) for i in ids]
                if isinstance(peer, raw.types.InputPeerChannel):
                    rpc = raw.functions.channels.GetMessages(channel=peer, id=ids)
                else:
                    rpc = raw.functions.messages.GetMessages(id=ids)

            r = await self.invoke(rpc, sleep_threshold=-1)

            messages = await utils.parse_messages(
                self,
                r,
                is_scheduled=is_scheduled,
                replies=replies
            )

            return messages if is_iterable else messages[0] if messages else None

        if link:
            linkps = link.split("/")
            raw_chat_id, message_thread_id, message_id = None, None, None
            if (
                len(linkps) == 7 and
                linkps[3] == "c"
            ):
                # https://t.me/c/1192302355/322/487
                raw_chat_id = utils.get_channel_id(
                    int(linkps[4])
                )
                message_thread_id = int(linkps[5])
                message_id = int(linkps[6])
            elif len(linkps) == 6:
                if linkps[3] == "c":
                    # https://t.me/c/1387666944/609282
                    raw_chat_id = utils.get_channel_id(
                        int(linkps[4])
                    )
                    message_id = int(linkps[5])
                else:
                    # https://t.me/TheForum/322/487
                    raw_chat_id = linkps[3]
                    message_thread_id = int(linkps[4])
                    message_id = int(linkps[5])

            elif (
                not self.me.is_bot and
                len(linkps) == 5 and
                linkps[3] == "m"
            ):
                r = await self.invoke(
                    raw.functions.account.ResolveBusinessChatLink(
                        slug=linkps[4]
                    )
                )
                users = {i.id: i for i in r.users}
                # chats = {i.id: i for i in r.chats}
                entities = [
                    types.MessageEntity._parse(
                        self, entity, users
                    )
                    for entity in getattr(r, "entities", [])
                ]
                entities = types.List(
                    filter(lambda x: x is not None, entities)
                )
                sender_chat = None
                cat_id = utils.get_raw_peer_id(r.peer)
                if isinstance(r.peer, raw.types.PeerUser):
                    sender_chat = types.Chat._parse_user_chat(self, users[cat_id])
                # elif isinstance(r.peer, raw.types.PeerChat):
                #     sender_chat = types.Chat._parse_chat_chat(self, chats[cat_id])
                # else:
                #     sender_chat = types.Chat._parse_channel_chat(
                #         self, chats[cat_id]
                #     )
                return types.Message(
                    id=0,  # TODO modify this later with a Draft type
                    text=Str(r.message).init(entities) or None,
                    entities=entities or None,
                    sender_chat=sender_chat,
                )

            elif len(linkps) == 5:
                # https://t.me/pyrogramchat/609282
                raw_chat_id = linkps[3]
                if raw_chat_id == "m":
                    raise ValueError(
                        "Invalid ClientType used to parse this message link"
                    )
                message_id = int(linkps[4])

            return await self.get_messages(
                chat_id=raw_chat_id,
                message_ids=message_id
            )

        raise ValueError("No argument supplied. Either pass link OR (chat_id, message_ids or reply_to_message_ids)")
