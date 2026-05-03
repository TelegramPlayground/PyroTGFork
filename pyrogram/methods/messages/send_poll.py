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
from datetime import datetime
from typing import Optional, Union

import pyrogram
from pyrogram import raw, utils, types, enums
from pyrogram.file_id import FileType

log = logging.getLogger(__name__)


class SendPoll:
    async def send_poll(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        question: "types.FormattedText",
        options: list["types.InputPollOption"],
        is_anonymous: bool = True,
        type: "enums.PollType" = enums.PollType.REGULAR,
        allows_multiple_answers: bool = None,
        allows_revoting: bool = None,
        shuffle_options: bool = None,
        allow_adding_options: bool = None,
        hide_results_until_closes: bool = None,
        correct_option_ids: list[int] = None,
        explanation: "types.FormattedText" = None,
        explanation_media: Optional[Union[
            "types.InputMediaAnimation",
            "types.InputMediaDocument",
            "types.InputMediaAudio",
            "types.InputMediaPhoto",
            "types.InputMediaSticker",
            "types.InputMediaVideo",
            "types.Location",
        ]] = None,
        open_period: int = None,
        close_date: datetime = None,
        is_closed: bool = None,
        description: "types.FormattedText" = None,
        description_media: Optional[Union[
            "types.InputMediaAnimation",
            "types.InputMediaDocument",
            "types.InputMediaAudio",
            "types.InputMediaPhoto",
            "types.InputMediaSticker",
            "types.InputMediaVideo",
            "types.Location",
        ]] = None,
        disable_notification: bool = None,
        protect_content: bool = None,
        allow_paid_broadcast: bool = None,
        paid_message_star_count: int = None,
        reply_parameters: "types.ReplyParameters" = None,
        message_thread_id: int = None,
        business_connection_id: str = None,
        send_as: Union[int, str] = None,
        schedule_date: datetime = None,
        message_effect_id: int = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None,
    ) -> "types.Message":
        """Send a native poll.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:

            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            question (:obj:`~pyrogram.types.FormattedText`):
                Poll question.
                **Users**: 1-255 characters.
                **Bots**: 1-300 characters.

            options (List of :obj:`~pyrogram.types.InputPollOption`):
                List of 1-12 poll answer options.

            is_anonymous (``bool``, *optional*):
                True, if the poll needs to be anonymous.
                Defaults to True.

            type (:obj:`~pyrogram.enums.PollType`, *optional*):
                Poll type, :obj:`~pyrogram.enums.PollType.QUIZ` or :obj:`~pyrogram.enums.PollType.REGULAR`.
                Defaults to :obj:`~pyrogram.enums.PollType.REGULAR`.

            allows_multiple_answers (``bool``, *optional*):
                True, if the poll allows multiple answers.
                Defaults to False.

            allows_revoting (``bool``, *optional*):
                Pass True, if the poll allows to change chosen answer options, defaults to False for quizzes and to True for regular polls.

            shuffle_options (``bool``, *optional*):
                Pass True, if the poll options must be shown in random order.

            allow_adding_options (``bool``, *optional*):
                Pass True, if answer options can be added to the poll after creation; not supported for anonymous polls and quizzes.

            hide_results_until_closes (``bool``, *optional*):
                Pass True, if poll results must be shown only after the poll closes.

            correct_option_ids (List of ``int``, *optional*):
                List of monotonically increasing 0-based identifiers of the correct answer options, required for polls in quiz mode.

            explanation (:obj:`~pyrogram.types.FormattedText`, *optional*):
                Text that is shown when a user chooses an incorrect answer or taps on the lamp icon in a quiz-style
                poll, 0-200 characters with at most 2 line feeds after entities parsing.

            explanation_media (:obj:`~pyrogram.types.InputMediaAnimation` | :obj:`~pyrogram.types.InputMediaDocument` | :obj:`~pyrogram.types.InputMediaAudio` | :obj:`~pyrogram.types.InputMediaPhoto` | :obj:`~pyrogram.types.InputMediaSticker` | :obj:`~pyrogram.types.InputMediaVideo` | :obj:`~pyrogram.types.Location`, *optional*):
                Media attached to the poll explanation that is shown when a user chooses an incorrect answer or taps on the lamp icon in a quiz-style poll.

            open_period (``int``, *optional*):
                Amount of time in seconds the poll will be active after creation, 5-2628000.
                Can't be used together with *close_date*.

            close_date (:py:obj:`~datetime.datetime`, *optional*):
                Point in time when the poll will be automatically closed.
                Must be at least 5 and no more than 2628000 seconds in the future.
                Can't be used together with *open_period*.

            is_closed (``bool``, *optional*):
                Pass True, if the poll needs to be immediately closed.
                This can be useful for poll preview.

            description (:obj:`~pyrogram.types.FormattedText`, *optional*):
                Description of the poll to be sent, 0-1024 characters after entities parsing.

            description_media (:obj:`~pyrogram.types.InputMediaAnimation` | :obj:`~pyrogram.types.InputMediaDocument` | :obj:`~pyrogram.types.InputMediaAudio` | :obj:`~pyrogram.types.InputMediaPhoto` | :obj:`~pyrogram.types.InputMediaSticker` | :obj:`~pyrogram.types.InputMediaVideo` | :obj:`~pyrogram.types.Location`, *optional*):
                Media attached to the poll.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            protect_content (``bool``, *optional*):
                Pass True if the content of the message must be protected from forwarding and saving; for bots only.

            allow_paid_broadcast (``bool``, *optional*):
                Pass True to allow the message to ignore regular broadcast limits for a small fee; for bots only

            paid_message_star_count (``int``, *optional*):
                The number of Telegram Stars the user agreed to pay to send the messages.

            reply_parameters (:obj:`~pyrogram.types.ReplyParameters`, *optional*):
                Description of the message to reply to

            message_thread_id (``int``, *optional*):
                If the message is in a thread, ID of the original message.

            business_connection_id (``str``, *optional*):
                Unique identifier of the business connection on behalf of which the message will be sent.

            send_as (``int`` | ``str``):
                Unique identifier (int) or username (str) of the chat or channel to send the message as.
                You can use this to send the message on behalf of a chat or channel where you have appropriate permissions.
                Use the :meth:`~pyrogram.Client.get_send_as_chats` to return the list of message sender identifiers, which can be used to send messages in the chat, 
                This setting applies to the current message and will remain effective for future messages unless explicitly changed.
                To set this behavior permanently for all messages, use :meth:`~pyrogram.Client.set_send_as_chat`.

            schedule_date (:py:obj:`~datetime.datetime`, *optional*):
                Date when the message will be automatically sent.

            message_effect_id (``int`` ``64-bit``, *optional*):
                Unique identifier of the message effect to be added to the message; for private chats only.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardRemove` | :obj:`~pyrogram.types.ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

        Returns:
            :obj:`~pyrogram.types.Message`: On success, the sent poll message is returned.

        Example:
            .. code-block:: python

                # Regular poll
                from pyrogram import types
                await app.send_poll(
                    chat_id=chat_id,
                    question=types.FormattedText(
                        text="Is this a poll question?"
                    ),
                    options=[
                        types.InputPollOption(
                            text=types.FormattedText(
                                text="Yes"
                            )
                        ),
                        types.InputPollOption(
                            text=types.FormattedText(
                                text="No"
                            )
                        ),
                    ]
                )


                # Poll with media
                await app.send_poll(
                    chat_id=chat_id,
                    question="Where we are?",
                    media=types.InputMediaPhoto("photo.jpg"),
                    options=[
                        types.InputPollOption(
                            text="Maybe here?",
                            media=types.InputMediaPhoto("photo1.jpg")
                        ),
                        types.InputPollOption(
                            text="Or here?",
                            media=types.Location(
                                longitude=49.807760,
                                latitude=73.088504
                            ),
                        ),
                    ]
                )

        """

        if isinstance(question, str):
            question = types.FormattedText(text=question)

        if isinstance(explanation, str):
            explanation = types.FormattedText(text=explanation)

        if isinstance(description, str):
            description = types.FormattedText(text=description)

        answers = []
        for i, answer_ in enumerate(options):
            if isinstance(answer_, str):
                answer_ = types.InputPollOption(
                    text=types.FormattedText(
                        text=answer_
                    )
                )
            answers.append(await answer_.write(self))

        raw_description = await description.write(self, None) if description else None
        solution = await explanation.write(self) if explanation else None

        reply_to = await utils._get_reply_message_parameters(
            self,
            message_thread_id,
            reply_parameters
        )

        if type == enums.PollType.QUIZ and allow_adding_options:
            allow_adding_options = False

        if type == enums.PollType.QUIZ and len(correct_option_ids) > 1 and not allows_multiple_answers:
            allows_multiple_answers = True

        attached_media = None
        if description_media:
            if isinstance(description_media, types.Location):
                attached_media = await description_media.write()
            else:
                attached_media, _ = await description_media.write(
                    client=self,
                    chat_id=chat_id,
                    business_connection_id=business_connection_id,
                )
        solution_media = None
        if explanation_media:
            if isinstance(explanation_media, types.Location):
                solution_media = await explanation_media.write()
            else:
                solution_media, _ = await explanation_media.write(
                    client=self,
                    chat_id=chat_id,
                    business_connection_id=business_connection_id,
                )

        rpc = raw.functions.messages.SendMedia(
            peer=await self.resolve_peer(chat_id),
            media=raw.types.InputMediaPoll(
                poll=raw.types.Poll(
                    id=self.rnd_id(),
                    hash=0,
                    question=await question.write(self),
                    answers=answers,
                    closed=is_closed,
                    public_voters=not is_anonymous,
                    multiple_choice=allows_multiple_answers,
                    quiz=type == enums.PollType.QUIZ or False,
                    close_period=open_period,
                    close_date=utils.datetime_to_timestamp(close_date),
                    open_answers=allow_adding_options,
                    revoting_disabled=not allows_revoting,
                    shuffle_answers=shuffle_options,
                    hide_results_until_close=hide_results_until_closes,
                    # creator:flags.10?true 
                ),
                correct_answers=correct_option_ids or None,
                solution=solution.text if solution else None,
                solution_entities=solution.entities if solution else None,
                solution_media=solution_media,
                attached_media=attached_media,
            ),
            message=raw_description.text if raw_description else "",
            entities=raw_description.entities if raw_description else None,
            silent=disable_notification,
            reply_to=reply_to,
            random_id=self.rnd_id(),
            send_as=await self.resolve_peer(send_as) if send_as else None,
            schedule_date=utils.datetime_to_timestamp(schedule_date),
            noforwards=protect_content,
            allow_paid_floodskip=allow_paid_broadcast,
            allow_paid_stars=paid_message_star_count,
            reply_markup=await reply_markup.write(self) if reply_markup else None,
            effect=message_effect_id
        )
        if business_connection_id:
            r = await self.invoke(
                raw.functions.InvokeWithBusinessConnection(
                    query=rpc,
                    connection_id=business_connection_id
                )
            )
        else:
            r = await self.invoke(rpc)

        for i in r.updates:
            if isinstance(
                i,
                (
                    raw.types.UpdateNewMessage,
                    raw.types.UpdateNewChannelMessage,
                    raw.types.UpdateNewScheduledMessage
                )
            ):
                return await types.Message._parse(
                    self, i.message,
                    {i.id: i for i in r.users},
                    {i.id: i for i in r.chats},
                    is_scheduled=isinstance(i, raw.types.UpdateNewScheduledMessage),
                    replies=self.fetch_replies
                )
            elif isinstance(
                i,
                (
                    raw.types.UpdateBotNewBusinessMessage
                )
            ):
                return await types.Message._parse(
                    self,
                    i.message,
                    {i.id: i for i in r.users},
                    {i.id: i for i in r.chats},
                    business_connection_id=getattr(i, "connection_id", business_connection_id),
                    raw_reply_to_message=i.reply_to_message,
                    replies=0
                )
