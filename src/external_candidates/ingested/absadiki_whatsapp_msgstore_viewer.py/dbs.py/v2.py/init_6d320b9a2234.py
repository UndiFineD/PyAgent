# Extracted from: C:\DEV\PyAgent\.external\absadiki-whatsapp-msgstore-viewer\dbs\v2\__init__.py
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Database interface for accessing and retrieving WhatsApp chat, message, and call data.


This module defines the `Database` class, which extends the `AbstractDatabase` to provide
methods for interacting with WhatsApp's SQLite databases. It facilitates the retrieval of
various data types, including:

- **Chats**: Fetches both individual and group chats with relevant details such as user
  information, last message content, and timestamps.

- **Messages**: Retrieves messages associated with a specific chat, including text data,
  media file paths, and quoted message details.

- **Calls**: Obtains call logs with information on call direction, type (video or audio),
  duration, and associated user details.

The `Database` class constructs SQL queries to extract this information, ensuring that the
retrieved data is organized and accessible for further processing or analysis.

Classes:
    Database: Extends `AbstractDatabase` to implement methods for fetching chats, messages,
              and call logs from WhatsApp's databases.

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.
This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.
"""

__author__ = "Voice-less"
__copyright__ = "Copyright 2025"
__credits__ = ["Voice-less"]
__date__ = "2025/04/02"
__deprecated__ = False
__license__ = "GPLv3"
__maintainer__ = "Voice-less"
__status__ = "Production"
__version__ = "1.0.0"

if __name__ == "__main__":
    pass
