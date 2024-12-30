#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present KurimuzonAkuma <https://github.com/KurimuzonAkuma>
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

import inspect
import aiosqlite  # aiosqlite==0.20.0
import os
import time
from typing import Any

from pyrogram import raw
from .storage import Storage
from .. import utils
from pathlib import Path

# language=SQLite
SCHEMA = """
CREATE TABLE sessions
(
    dc_id     INTEGER PRIMARY KEY,
    api_id    INTEGER,
    test_mode INTEGER,
    auth_key  BLOB,
    date      INTEGER NOT NULL,
    user_id   INTEGER,
    is_bot    INTEGER
);

CREATE TABLE peers
(
    id             INTEGER PRIMARY KEY,
    access_hash    INTEGER,
    type           INTEGER NOT NULL,
    phone_number   TEXT,
    last_update_on INTEGER NOT NULL DEFAULT (CAST(STRFTIME('%s', 'now') AS INTEGER))
);

CREATE TABLE usernames
(
    id       INTEGER,
    username TEXT,
    FOREIGN KEY (id) REFERENCES peers(id)
);

CREATE TABLE update_state
(
    id   INTEGER PRIMARY KEY,
    pts  INTEGER,
    qts  INTEGER,
    date INTEGER,
    seq  INTEGER
);

CREATE TABLE version
(
    number INTEGER PRIMARY KEY
);

CREATE INDEX idx_peers_id ON peers (id);
CREATE INDEX idx_peers_phone_number ON peers (phone_number);
CREATE INDEX idx_usernames_username ON usernames (username);

CREATE TRIGGER trg_peers_last_update_on
    AFTER UPDATE
    ON peers
BEGIN
    UPDATE peers
    SET last_update_on = CAST(STRFTIME('%s', 'now') AS INTEGER)
    WHERE id = NEW.id;
END;
"""


def get_input_peer(peer_id: int, access_hash: int, peer_type: str):
    if peer_type in ["user", "bot"]:
        return raw.types.InputPeerUser(
            user_id=peer_id,
            access_hash=access_hash
        )

    if peer_type == "group":
        return raw.types.InputPeerChat(
            chat_id=-peer_id
        )

    if peer_type in ["channel", "supergroup"]:
        return raw.types.InputPeerChannel(
            channel_id=utils.get_channel_id(peer_id),
            access_hash=access_hash
        )

    raise ValueError(f"Invalid peer type: {peer_type}")


class AioSQLiteStorage(Storage):
    VERSION = 5
    USERNAME_TTL = 8 * 60 * 60

    def __init__(self, name: str):
        super().__init__(name)

        self.conn = None  # type: aiosqlite.Connection

    async def update(self):
        version = await self.version()

        if version == 1:
            await self.conn.execute("DELETE FROM peers")
            await self.conn.commit()

        version += 1

        if version == 2:
            await self.conn.execute("ALTER TABLE sessions ADD api_id INTEGER")
            await self.conn.commit()

        version += 1

        if version == 3:
            await self.conn.executescript(USERNAMES_SCHEMA)
            await self.conn.commit()

        version += 1

        if version == 4:
            await self.conn.executescript(UPDATE_STATE_SCHEMA)
            await self.conn.commit()

        version += 1

        await self.version(version)

    async def create(self):
        await self.conn.executescript(SCHEMA)

        await self.conn.execute(
            "INSERT INTO version VALUES (?)",
            (self.VERSION,)
        )

        await self.conn.execute(
            "INSERT INTO sessions VALUES (?, ?, ?, ?, ?, ?, ?)",
            (2, None, None, None, 0, None, None)
        )
        await self.conn.commit()

    async def open(self):
        path = Path(self.name)
        file_exists = path.is_file()

        self.conn = await aiosqlite.connect(str(path), timeout=1, check_same_thread=False)

        await self.conn.execute("PRAGMA journal_mode=WAL")

        if not file_exists:
            await self.create()
        else:
            await self.update()

        await self.conn.execute("VACUUM")
        await self.conn.commit()

    async def save(self):
        await self.date(int(time.time()))
        await self.conn.commit()

    async def close(self):
        await self.conn.close()

    async def delete(self):
        os.remove(self.name)

    async def update_peers(self, peers: list[tuple[int, int, str, list[str], str]]):
        for peer_data in peers:
            id, access_hash, type, usernames, phone_number = peer_data

            await self.conn.execute(
                "REPLACE INTO peers (id, access_hash, type, phone_number)"
                "VALUES (?, ?, ?, ?)",
                (id, access_hash, type, phone_number)
            )

            await self.conn.execute(
                "DELETE FROM usernames WHERE id = ?",
                (id,)
            )

            await self.conn.executemany(
                "REPLACE INTO usernames (id, username) VALUES (?, ?)",
                [(id, username) for username in usernames] if usernames else [(id, None)]
            )

    async def update_state(self, value: tuple[int, int, int, int, int] = object):
        if value == object:
            q = await self.conn.execute(
                "SELECT id, pts, qts, date, seq FROM update_state"
            )
            return await q.fetchall()
        else:
            if value is None:
                await self.conn.execute(
                    "DELETE FROM update_state"
                )
            else:
                await self.conn.execute(
                "REPLACE INTO update_state (id, pts, qts, date, seq)"
                "VALUES (?, ?, ?, ?, ?)",
                value
            )
            await self.conn.commit()

    async def get_peer_by_id(self, peer_id: int):
        q = await self.conn.execute(
            "SELECT id, access_hash, type FROM peers WHERE id = ?",
            (peer_id,)
        )

        r = await q.fetchone()

        if r is None:
            raise KeyError(f"ID not found: {peer_id}")

        return get_input_peer(*r)

    async def get_peer_by_username(self, username: str):
        q = await self.conn.execute(
            "SELECT p.id, p.access_hash, p.type, p.last_update_on FROM peers p "
            "JOIN usernames u ON p.id = u.id "
            "WHERE u.username = ? "
            "ORDER BY p.last_update_on DESC",
            (username,)
        )

        r = await q.fetchone()

        if r is None:
            raise KeyError(f"Username not found: {username}")

        if abs(time.time() - r[3]) > self.USERNAME_TTL:
            raise KeyError(f"Username expired: {username}")

        return get_input_peer(*r[:3])

    async def get_peer_by_phone_number(self, phone_number: str):
        q = await self.conn.execute(
            "SELECT id, access_hash, type FROM peers WHERE phone_number = ?",
            (phone_number,)
        )

        r = await q.fetchone()

        if r is None:
            raise KeyError(f"Phone number not found: {phone_number}")

        return get_input_peer(*r)

    async def _get(self):
        attr = inspect.stack()[2].function

        r = await self.conn.execute(
            f"SELECT {attr} FROM sessions"
        )
        return (await r.fetchone())[0]

    async def _set(self, value: Any):
        attr = inspect.stack()[2].function

        await self.conn.execute(
            f"UPDATE sessions SET {attr} = ?",
            (value,)
        )
        await self.conn.commit()

    async def _accessor(self, value: Any = object):
        return await self._get() if value == object else await self._set(value)

    async def dc_id(self, value: int = object):
        return await self._accessor(value)

    async def api_id(self, value: int = object):
        return await self._accessor(value)

    async def test_mode(self, value: bool = object):
        return await self._accessor(value)

    async def auth_key(self, value: bytes = object):
        return await self._accessor(value)

    async def date(self, value: int = object):
        return await self._accessor(value)

    async def user_id(self, value: int = object):
        return await self._accessor(value)

    async def is_bot(self, value: bool = object):
        return await self._accessor(value)

    async def version(self, value: int = object):
        if value == object:
            q = await self.conn.execute(
                "SELECT number FROM version"
            )

            return (await q.fetchone())[0]
        else:
            await self.conn.execute(
                "UPDATE version SET number = ?",
                (value,)
            )
            await self.conn.commit()
