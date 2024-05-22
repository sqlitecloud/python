import os
import sqlite3
import tempfile

import pytest

from sqlitecloud import download
from sqlitecloud.client import SqliteCloudClient
from sqlitecloud.types import SQCLOUD_ERRCODE, SQCloudConnect, SQCloudException, SqliteCloudAccount


class TestDownload:
    def test_download_database(self, sqlitecloud_connection):
        connection, _ = sqlitecloud_connection

        temp_file = tempfile.mkstemp(prefix="chinook")[1]
        download.download_db(connection, "chinook.sqlite", temp_file)

        db = sqlite3.connect(temp_file)
        cursor = db.execute("SELECT * FROM albums")

        assert cursor.description[0][0] == "AlbumId"
        assert cursor.description[1][0] == "Title"

    def test_download_missing_database(self, sqlitecloud_connection):
        connection, _ = sqlitecloud_connection

        temp_file = tempfile.mkstemp(prefix="missing")[1]

        with pytest.raises(SQCloudException) as e:
            download.download_db(connection, "missing.sqlite", temp_file)

        assert e.value.errcode == SQCLOUD_ERRCODE.COMMAND.value
        assert e.value.errmsg == "Database missing.sqlite does not exist."