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

from datetime import datetime
from typing import Union, Optional

import pyrogram
from pyrogram import enums, raw, types, utils
from ..object import Object
from ..update import Update
from .message import Str


class Poll(Object, Update):
    """A Poll.

    Parameters:
        id (``str``):
            Unique poll identifier.

        question (:obj:`~pyrogram.types.FormattedText`):
            Poll question, 1-255 characters.

        options (List of :obj:`~pyrogram.types.PollOption`):
            List of poll options.

        total_voter_count (``int``):
            Total number of users that voted in the poll.

        is_closed (``bool``):
            True, if the poll is closed.

        is_anonymous (``bool``):
            True, if the poll is anonymous

        type (:obj:`~pyrogram.enums.PollType`):
            Poll type.

        allows_multiple_answers (``bool``):
            True, if the poll allows multiple answers.

        allows_revoting (``bool``):
            True, if the poll allows to change the chosen answer options.

        chosen_option_id (``int``, *optional*):
            0-based index of the chosen option), None in case of no vote yet.

        correct_option_ids (List of ``int``, *optional*):
            Array of 0-based identifiers of the correct answer options.
            Available only for polls in quiz mode which are closed or were sent (not forwarded) by the bot or to the private chat with the bot.

        explanation (:obj:`~pyrogram.types.FormattedText`, *optional*):
            Text that is shown when a user chooses an incorrect answer or taps on the lamp icon in a quiz-style poll,
            0-200 characters.

        open_period (``int``, *optional*):
            Amount of time in seconds the poll will be active after creation.

        close_date (:py:obj:`~datetime.datetime`, *optional*):
            Point in time when the poll will be automatically closed.

        description (:obj:`~pyrogram.types.FormattedText`, *optional*):
            Description of the poll; for polls inside the Message object only.

    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        id: str,
        question: "types.FormattedText",
        options: list["types.PollOption"],
        total_voter_count: int,
        is_closed: bool,
        is_anonymous: bool,
        type: "enums.PollType",
        allows_multiple_answers: bool,
        allows_revoting: bool,
        chosen_option_id: Optional[int] = None,
        correct_option_ids: Optional[list[int]] = None,
        explanation: Optional["types.FormattedText"] = None,
        open_period: Optional[int] = None,
        close_date: Optional[datetime] = None,
        description: Optional["types.FormattedText"] = None,
    ):
        super().__init__(client)

        self.id = id
        self.question = question
        self.options = options
        self.total_voter_count = total_voter_count
        self.is_closed = is_closed
        self.is_anonymous = is_anonymous
        self.type = type
        self.allows_multiple_answers = allows_multiple_answers
        self.allows_revoting = allows_revoting
        self.chosen_option_id = chosen_option_id
        self.correct_option_ids = correct_option_ids
        self.explanation = explanation
        self.open_period = open_period
        self.close_date = close_date
        self.description = description

    @staticmethod
    async def _parse(
        client,
        media_poll: Union[
            "raw.types.MessageMediaPoll",
            "raw.types.UpdateMessagePoll"
        ],
        users: dict,
        chats: dict,
    ) -> "Poll":
        poll: raw.types.Poll = media_poll.poll
        poll_results: raw.types.PollResults = media_poll.results
        results: list[raw.types.PollAnswerVoters] = poll_results.results

        persistent_id = ""
        if isinstance(media_poll, raw.types.UpdateMessagePoll):
            persistent_id = str(media_poll.poll_id)
        if isinstance(media_poll, raw.types.MessageMediaPoll):
            persistent_id = str(poll.id)

        chosen_option_id = []
        correct_option_ids = []
        options = []

        for i, answer in enumerate(poll.answers):
            voter_count = 0

            if results:
                result = results[i]
                voter_count = result.voters

                if result.chosen:
                    chosen_option_id.append(i)

                if result.correct:
                    correct_option_ids.append(i)

            added_by_peer = answer.added_by
            user = None
            voter_chat = None

            if added_by_peer:
                if isinstance(added_by_peer, raw.types.PeerUser):
                    user = types.Chat._parse_user_chat(client, users[added_by_peer.user_id])

                elif isinstance(added_by_peer, raw.types.PeerChat):
                    voter_chat = types.Chat._parse_chat_chat(client, chats[added_by_peer.chat_id])

                else:
                    voter_chat = types.Chat._parse_channel_chat(client, chats[added_by_peer.channel_id])

            options.append(
                types.PollOption(
                    persistent_id=answer.option.decode("UTF-8"),
                    text=types.FormattedText._parse(client, answer.text),
                    # media:flags.0?MessageMedia
                    voter_count=voter_count,
                    data=answer.option,
                    added_by_user=user,
                    added_by_chat=voter_chat,
                    addition_date=utils.timestamp_to_datetime(answer.date),
                    client=client
                )
            )

        return Poll(
            id=persistent_id,
            question=types.FormattedText._parse(
                client,
                poll.question
            ),
            options=options,
            total_voter_count=poll_results.total_voters,
            is_closed=poll.closed,
            is_anonymous=not poll.public_voters,
            type=enums.PollType.QUIZ if poll.quiz else enums.PollType.REGULAR,
            allows_multiple_answers=poll.multiple_choice,
            allows_revoting=not poll.revoting_disabled,
            chosen_option_id=chosen_option_id,
            correct_option_ids=correct_option_ids,
            explanation=types.FormattedText._parse(client, raw.types.TextWithEntities(text=poll_results.solution, entities=poll_results.solution_entities)),
            open_period=poll.close_period,
            close_date=utils.timestamp_to_datetime(poll.close_date),
            description=None, #types.FormattedText._parse(client, ),
            client=client
        )

    @staticmethod
    async def _parse_update(
        client,
        update: Union["raw.types.UpdateMessagePoll", "raw.types.UpdateMessagePollVote"],
        users: dict,
        chats: dict,
    ):
        if isinstance(update, raw.types.UpdateMessagePoll):
            if update.poll is not None:
                return await Poll._parse(client, update, users, chats)

            # TODO: FIXME!
            results = update.results.results
            chosen_option_id = []
            correct_option_id = []
            options = []
            question = types.FormattedText(
                text=""
            )

            for i, result in enumerate(results):
                if result.chosen:
                    chosen_option_id.append(i)

                if result.correct:
                    correct_option_ids.append(i)

                options.append(
                    types.PollOption(
                        persistent_id=result.option.decode("UTF-8"),
                        text=None,
                        # media:flags.0?MessageMedia
                        voter_count=result.voters,
                        data=result.option,
                        client=client
                    )
                )

            return Poll(
                id=str(update.poll_id),
                question=question,
                options=options,
                total_voter_count=update.results.total_voters,
                is_closed=False,
                chosen_option_id=chosen_option_id,
                correct_option_id=correct_option_id,
                client=client
            )

    async def stop(
        self,
        reply_markup: "types.InlineKeyboardMarkup" = None,
        business_connection_id: str = None
    ) -> "types.Poll":
        """Bound method *stop* of :obj:`~pyrogram.types.Poll`.

        Use as a shortcut for:

        .. code-block:: python

            client.stop_poll(
                chat_id=message.chat.id,
                message_id=message_id,
            )

        Parameters:
            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup`, *optional*):
                An InlineKeyboardMarkup object.

            business_connection_id (``str``, *optional*):
                Unique identifier of the business connection on behalf of which the message to be edited was sent

        Example:
            .. code-block:: python

                message.poll.stop()

        Returns:
            :obj:`~pyrogram.types.Poll`: On success, the stopped poll with the final results is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """

        return await self._client.stop_poll(
            chat_id=self.chat.id,
            message_id=self.message_id,
            reply_markup=reply_markup,
            business_connection_id=business_connection_id
        )
