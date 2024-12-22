"""
	HangoutCore Module Script.
	----------
	Last Updated: June 24, 2024
	Last Updated by: Lino
	License: Refer to LICENSE.md
	Notes:
		None
	━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	This script handles the following:
	----------
	Terminal Manipulation/Handling
	━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	WARNING: This is a Core Script
		› Please do not modify any of the following content unless you know what you're doing. Modifying the following code and not updating the rest of the bot 
			code to match can/will cause issues.
		› If you do decide to modify the following code please understand that HangoutCore's Dev team, Discord.py's Dev Team nor Python's Dev team are obligated
			to help you.
		› By Modifying the following code you acknowledge and agree to the text above.
	━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import json

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Section Title: Dependencies
import aiomysql
import discord

import hangoutcore

# # from .terminal import Terminal
# from typing import Optional, Union

# # terminal = Terminal(f"Hangoutcore.Database", hangoutcore.loggerHangoutCore)
# # log = terminal.Log(f"Hangoutcore.Database", hangoutcore.loggerHangoutCore)
# # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# # Section Title: Default Variables

# error_configbot = "Unable To Access Bot Configuration / Invalid Bot Configuration. Please check configuration."
# error_db_pool = "Unable To Access Database Pool / Invalid Database Pool. Please check configuration."

guildTemplate = {
    "version": "0.1.2",
    "roles": {
        "guild_muted": 0,
        "guild_trial_moderator": 0,
        "guild_moderator": 0,
        "guild_administrator": 0,
        "guild_owner": 0,
    },
    "channels": {},
    "guild_rules": "",
    "guild_blacklisted": False,
    "extras": {
        "guild_announcements": {
            "member_join": {"enabled": False, "message": ""},
            "member_rejoin": {"enabled": False, "message": ""},
            "member_left": {"enabled": False, "message": ""},
            "member_banned": {"enabled": False, "message": ""},
            "member_kicked": {"enabled": False, "message": ""},
        },
        "guild_applications": {
            "enabled": False,
            "channel": 0,
            "roles": [{"role_name": "", "role_id": 0}],
        },
        "guild_autoroles": {"enabled": False, "roles": []},
        "guild_bot_announcements": {"enabled": False, "channel": 0},
        "guild_economy": {
            "enabled": False,
            "name": "",
            "currency": "",
            "channel": 0,
            "message": 0,
            "starting_balance": 1000,
        },
        "guild_level": {"enabled": False, "announce": False, "channel": 0},
        "guild_selfroles": {"enabled": False, "channel": 0, "message": 0, "roles": []},
        "guild_stats": {
            "enabled": False,
            "am_channel": 0,
            "t_channel": 0,
            "b_channel": 0,
            "display": {"active_members": False, "total_members": False, "bots": False},
        },
        "guild_staff_announcements": {
            "enabled": False,
            "channel": 0,
            "user_events": {
                "member_join": False,
                "member_remove": False,
                "member_update": False,
                "user_update": False,
                "private_channel_create": False,
                "private_channel_delete": False,
                "private_channel_update": False,
            },
            "guild_events": {
                "guild_channel_create": False,
                "guild_channel_delete": False,
                "guild_channel_update": False,
                "guild_channel_pins_update": False,
                "guild_join": False,
                "guild_remove": False,
                "guild_update": False,
                "guild_role_create": False,
                "guild_role_delete": False,
                "guild_role_update": False,
                "guild_emojis_update": False,
                "guild_available": False,
                "guild_unavailable": False,
            },
        },
        "guild_suggestions": {"enabled": False, "channel": 0, "allow_vote": False},
        "guild_tickets": {"enabled": False, "channel": 0, "role_staff": 0},
        "guild_verification": {
            "enabled": False,
            "channel": 0,
            "message": 0,
            "role": 0,
            "verified_users": [],
        },
        "guild_voice_lobby": {"enabled": False, "channels": []},
    },
}

userTemplate = {
    "version": "0.1.2",
    "guilds": [],
    "disable_levelup_notifications": False,
    "bot": {
        "blacklisted": False,
        "reason": "",
        "reports": [],
        "bans": [],
        "kicks": [],
        "command_stats": {},
    },
}

# # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# # Section Title: Generic Database Functions


async def updateTableRow(table, row, data) -> dict | None:
    log = hangoutcore.log

    if hangoutcore.DB_POOL is None:
        return None

    async with hangoutcore.DB_POOL.acquire() as _connection:
        _connection: aiomysql.Connection
        async with _connection.cursor() as _cursor:
            _cursor: aiomysql.Cursor

            try:
                await _cursor.execute(
                    f"""
				CREATE TABLE IF NOT EXISTS `{table}` (
					id BIGINT PRIMARY KEY UNIQUE NOT NULL,
					name TEXT,
					data JSON
				)
				"""
                )
            except Exception as err:
                log.ERROR({err})
            else:
                await _connection.commit()

            try:
                await _cursor.execute(f"SELECT * FROM `{table}` WHERE id = %s", (row,))
                _result = await _cursor.fetchone()
            except Exception as err:
                log.ERROR({err})
            else:
                if _result is not None:
                    try:
                        _result = await _cursor.execute(
                            f"""
						UPDATE `{table}` 
						SET name = %s, data = %s 
						WHERE id = %s
						""",
                            (data["name"], json.dumps(data["data"]), row),
                        )
                        await _connection.commit()
                        await _cursor.execute(
                            f"SELECT * FROM `{table}` WHERE id = %s", (row,)
                        )
                    except Exception as err:
                        log.ERROR({err})
                    else:
                        _result = await _cursor.fetchone()

                        return _result
                else:
                    pass  # create new entry if none

        # if _result is None:
        # 	try:
        # 		_result = await _cursor.execute(f"""\
        # 				INSERT INTO users
        # 				(id, name, data)
        # 				VALUES( %s, %s, %s)
        # 				""", (int(user.id), user.name, json.dumps(data)))
        # 	except Exception as e:
        # 		log.WARNING(f"Func {registerGuild.__name__} Failed: {e}")
        # 	else:
        # 		await _connection.commit()
        # 		log.INFO(f"Successfully created a database entry for user: {user.name}")
        # 		return
        # else:


async def retrieveTableColumn(table, column) -> dict | None:
    """Function used to retreive info from our database.
    Creates a new table if one does not exist.
    ------------
    table:
            Name of database table to use for our column data.
    column:
            Name of table column to fetch.
    """
    log = hangoutcore.log

    if hangoutcore.DB_POOL is None:
        return None

    async with hangoutcore.DB_POOL.acquire() as _connection:
        _connection: aiomysql.Connection
        async with _connection.cursor() as _cursor:
            _cursor: aiomysql.Cursor
            try:
                await _cursor.execute(f"SELECT {column} FROM {table}")
            except Exception as e:
                log.WARNING(f"{e}")
                return None
            _result = await _cursor.fetchall()
            _data = []
            if _result is not None:
                for entry in _result:
                    _data.append(entry[0])
                return _data
            else:
                return None


async def retrieveTableRow(table, row) -> dict | None:
    """Function used to retreive info from our database.
    Creates a new table if one does not exist.
    ------------
    table:
            Name of database table to use for our column data.
    column:
            Name of table column to fetch.
    """
    log = hangoutcore.log

    if hangoutcore.DB_POOL is None:
        return None

    async with hangoutcore.DB_POOL.acquire() as _connection:
        _connection: aiomysql.Connection
        async with _connection.cursor() as _cursor:
            _cursor: aiomysql.Cursor
            try:
                await _cursor.execute(f"SELECT * FROM {table} WHERE id = ({row})")
            except Exception as e:
                log.ERROR(f"{e}")
                return None
            _result = await _cursor.fetchone()
            if _result is not None:
                _data = {
                    "id": int(_result[0]),
                    "name": _result[1],
                    "data": json.loads(_result[2]),
                }
                return _data
            else:
                return None


async def closePool():
    log = hangoutcore.log

    if hangoutcore.DB_POOL.closed:
        log.WARNING(f"Database Pool Closed.")
        return True

    try:
        await hangoutcore.DB_POOL.clear()
        hangoutcore.DB_POOL.close()
        await hangoutcore.DB_POOL.wait_closed()
    except Exception as err:
        log.ERROR(err)
        return False
    else:
        if hangoutcore.DB_POOL.closed:
            log.WARNING(f"Database Pool Now Closed.")
        return True


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Section Title: Guild Related Database Functions

# async def registerGuild(guild: discord.Guild) -> dict | None:
#     """Function used to register guilds to our database.
#     Creates a new table if one does not exist.
#     ------------
#     guild: discord.Guild
#         Guild being registered.
#     """
#     # Critical Prechecks to avoid future headaches...
#     if hangoutcore.CONFIG_BOT is None:
#         log.CRITICAL(f"Func {registerGuild.__name__} Failed: {error_configbot}")
#         return None
#     if hangoutcore.DB_POOL is None:
#         log.ERROR(f"Func {registerGuild.__name__} Failed: {error_db_pool}")
#         return None

#     # Finally connect to Database
#     async with hangoutcore.DB_POOL.get() as _connection:
#         _connection: aiomysql.Connection
#         async with _connection.cursor() as _cursor:
#             _cursor: aiomysql.Cursor

#             try:
#                 await _cursor.execute("""\
#                     CREATE TABLE IF NOT EXISTS guilds
#                     (id BIGINT PRIMARY KEY UNIQUE NOT NULL, name text, data JSON)""")
#             except Exception as e:
#                 log.ERROR(f"{e}")
#             else:
#                 await _connection.commit()

#             try:
#                 await _cursor.execute(f"""\
#                     SELECT * FROM guilds
#                     WHERE id = (%s)
#                     """,(guild.id))
#             except Exception as e:
#                 log.WARNING(f"{e}")

#             _result = await _cursor.fetchone()

#             if _result is None:
#                 try:
#                     _result = await _cursor.execute(f"""\
#                             INSERT INTO guilds
#                             (id, name, data)
#                             VALUES( %s, %s, %s)
#                             """, (int(guild.id), guild.name, json.dumps(guildTemplate)))
#                 except Exception as e:
#                     log.WARNING(f"{e}")
#                 else:
#                     log.INFO(f"Successfully created a database entry for guild: {guild.name}")
#                     await _connection.commit()


async def retrieveGuild(guild: discord.Guild | int) -> dict | None:
    """Function used to fetch guild info from our database.
    ------------
    guild: discord.Guild
            Guild being registered.
    """
    _guildID = guild

    if type(guild) == discord.Guild:
        _guildID = guild.id

    try:
        _data = await retrieveTableRow("guilds", _guildID)
    except Exception as err:
        hangoutcore.log.ERROR(err)
        return None
    else:
        return _data[2]


# async def updateGuild(guild: discord.Guild, data = None) -> dict | None:
#     """Function used to update guild info in our database.
#     Creates a new entry if one does not exist.
#     ------------
#     guild: discord.Guild
#         Guild being registered.
#     """
#     if hangoutcore.CONFIG_BOT is None:
#         log.CRITICAL(f"Func {registerGuild.__name__} Failed: {error_configbot}")
#         return None
#     if hangoutcore.DB_POOL is None:
#         log.ERROR(f"Func {registerGuild.__name__} Failed: {error_db_pool}")
#         return None

#     async with hangoutcore.DB_POOL.get() as _connection:
#         _connection: aiomysql.Connection
#         async with _connection.cursor() as _cursor:
#             _cursor: aiomysql.Cursor

#             if data is None:
#                 data = guildTemplate
#                 _tmpr = ",\n"
#                 log.DEBUG(f"New Guild Data: {str(data).replace(',', _tmpr)}")

#             try:
#                 await _cursor.execute(f"""\
#                     SELECT * FROM guilds
#                     WHERE id = (%s)
#                     """,(guild.id))
#             except Exception as e:
#                 log.WARNING(f"{e}")

#             _result = await _cursor.fetchone()

#             if _result is None:
#                 try:
#                     _result = await _cursor.execute(f"""\
#                             INSERT INTO guilds
#                             (id, name, data)
#                             VALUES( %s, %s, %s)
#                             """, (int(guild.id), guild.name, json.dumps(data)))
#                 except Exception as e:
#                     log.WARNING(f"{e}")
#                 else:
#                     await _connection.commit()
#                     log.INFO(f"Successfully created a database entry for guild: {guild.name}")
#                     return
#             else:
#                 if data['version'] != guildTemplate['version']:
#                     log.WARNING(f"Guild Data is out of date for {guild.name}")
#                     pass

#                 try:
#                     _result = await _cursor.execute(f"""\
#                             UPDATE guilds SET name = %s, data = %s
#                             WHERE id = %s"""
#                             , (guild.name, json.dumps(data), guild.id))
#                 except Exception as e:
#                     log.WARNING(f"{e}")
#                 else:
#                     await _connection.commit()
#                     log.INFO(f"Successfully updated database entry for guild: {guild.name}")
#                     return

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Section Title: User Related Database Functions

# async def registerUser(user) -> dict | None:
#     if hangoutcore.CONFIG_BOT is None:
#         log.CRITICAL(f"Func {registerGuild.__name__} Failed: {error_configbot}")
#         return None
#     if hangoutcore.DB_POOL is None:
#         log.ERROR(f"Func {registerGuild.__name__} Failed: {error_db_pool}")
#         return None

#     async with hangoutcore.DB_POOL.get() as _connection:
#         _connection: aiomysql.Connection
#         async with _connection.cursor() as _cursor:
#             _cursor: aiomysql.Cursor

#             try:
#                 await _cursor.execute("""\
#                     CREATE TABLE IF NOT EXISTS users
#                     (id BIGINT PRIMARY KEY UNIQUE NOT NULL, name text, data JSON)""")
#             except Exception as e:
#                 log.WARNING(f"{e}")
#             else:
#                 await _connection.commit()

#             try:
#                 await _cursor.execute(f"""\
#                     SELECT * FROM users
#                     WHERE id = (%s)
#                     """,(user.id))
#             except Exception as e:
#                 log.WARNING(f"{e}")

#             _result = await _cursor.fetchone()
#             if _result is None:
#                 try:
#                     _result = await _cursor.execute(f"""\
#                             INSERT INTO users
#                             (id, name, data)
#                             VALUES( %s, %s, %s)
#                             """, (int(user.id), user.name, json.dumps(userTemplate)))
#                 except Exception as e:
#                     log.WARNING(f"{e}")
#                 else:
#                     await _connection.commit()
#                     log.INFO(f"Successfully created a database entry for member: {user.name}")


async def retrieveUser(user: discord.Member | discord.User | int) -> dict | None:
    """Function used to fetch user info from our database.
    ------------
    user: discord.User | discord.Member | int
            User or user ID being fetched.
    """

    _userID = user

    if type(user) == discord.User or type(user) == discord.Member:
        _userID = user.id

    try:
        _data = await retrieveTableRow("users", _userID)
    except Exception as err:
        hangoutcore.log.ERROR(err)
        return None
    else:
        return _data[2]


# async def updateUser(user, data = None) -> dict | None:
#     if hangoutcore.CONFIG_BOT is None:
#         log.CRITICAL(f"Func {registerGuild.__name__} Failed: {error_configbot}")
#         return None
#     if hangoutcore.DB_POOL is None:
#         log.ERROR(f"Func {registerGuild.__name__} Failed: {error_db_pool}")
#         return None

#     async with hangoutcore.DB_POOL.get() as _connection:
#         _connection: aiomysql.Connection
#         async with _connection.cursor() as _cursor:
#             _cursor: aiomysql.Cursor

#             if data is None:
#                 data = userTemplate
#                 _tmpr = ",\n"
#                 log.DEBUG(f"New User Data: {str(data).replace(',', _tmpr)}")

#             try:
#                 await _cursor.execute(f"""\
#                     SELECT * FROM users
#                     WHERE id = (%s)
#                     """,(user.id))
#             except Exception as e:
#                 log.WARNING(f"{e}")

#             _result = await _cursor.fetchone()

#             if _result is None:
#                 try:
#                     _result = await _cursor.execute(f"""\
#                             INSERT INTO users
#                             (id, name, data)
#                             VALUES( %s, %s, %s)
#                             """, (int(user.id), user.name, json.dumps(data)))
#                 except Exception as e:
#                     log.WARNING(f"Func {registerGuild.__name__} Failed: {e}")
#                 else:
#                     await _connection.commit()
#                     log.INFO(f"Successfully created a database entry for user: {user.name}")
#                     return
#             else:
#                 if data['version'] != userTemplate['version']:
#                     log.WARNING(f"Guild Data is out of date for {user.name}")
#                     pass

#                 try:
#                     _result = await _cursor.execute(f"""\
#                             UPDATE users SET name = %s, data = %s
#                             WHERE id = %s"""
#                             , (user.name, json.dumps(data), user.id))
#                 except Exception as e:
#                     log.WARNING(f"Func {registerGuild.__name__} Failed: {e}")
#                 else:
#                     await _connection.commit()
#                     log.DEBUG(f"Successfully updated database entry for user: {user.name}")
#                     return

# async def updateUserRank(guild: discord.Guild, user: discord.User | discord.Member, amount: int):
#     log.DEBUG(f"{user} recieved {amount} xp")

#     _userData = await retrieveUser(user)
#     if _userData is None: # if for whatever reason we failed to retreive data, return
#         return

#     if _userData['bot']['blacklisted']: # User should not have gotten here while blacklisted but we check just in case.
#         return

#     _gainedGlobalLevels = 0
#     _gainedGuildLevels = 0

#     def processExperience(xp: int = 0, level: int = 1) -> dict[str, int]:
#         if level < 1: # Level should never be below 0
#             level = 1

#         _requiredExp = 1500 * level
#         _gainedLevels = 0
#         # _needsBalance = False

#         # if level == 1:
#         #     _needsBalance = False

#         while xp >= _requiredExp:
#             level += 1
#             _gainedLevels += 1
#             xp -= _requiredExp
#             _requiredExp = 1500 * level

#         # if _needsBalance: # Don't count our first level as a 'level up' since we start there
#         #     level -= 1
#         #     _gainedLevels -= 1

#         return {"experience": xp, "level": level, "gained": _gainedLevels}

#     # process global rank

#     _level = _userData['rank']['level'] # type: ignore
#     _experience = _userData['rank']['experience'] + amount # type: ignore

#     _newGlobalRank = processExperience(_experience, _level)

#     _userData['rank']['level'] = _newGlobalRank['level']
#     _userData['rank']['experience'] = _newGlobalRank['experience']
#     _gainedGlobalLevels += _newGlobalRank['gained']

#     # Process guild rank next
#     _guildData: dict = await retrieveGuild(guild) # type: ignore

#     if _guildData is None:
#         return

#     if _guildData['extras']['guild_level']['enabled']:
#         _guildEntry: dict = None # type: ignore

#         if len(_userData['rank']['guilds']) > 0:
#             for _entry in _userData['rank']['guilds']: # filter through user's guild ranks and locate our desired guild
#                 log.DEBUG(f"{_entry}")
#                 if _entry['id'] == guild.id:
#                     _guildEntry = _entry # set our guild specific rank to variable so we can update

#         log.DEBUG(f"1")
#         if _guildEntry is None: # type: ignore
#             log.DEBUG(f"a")
#             _newGuildRank = processExperience(amount)
#             _tmp: dict = {
#                 'id': guild.id,
#                 'experience': _newGuildRank['experience'],
#                 'level': _newGuildRank['level'],
#             }

#             _gainedGuildLevels += _newGuildRank['gained']

#             _userData['rank']['guilds'].append(_tmp)
#         else:
#             log.DEBUG(f"b")
#             _level = _guildEntry['level'] # type: ignore
#             _experience = _guildEntry['experience'] + amount # type: ignore

#             _newGuildRank = processExperience(_experience, _level)

#             _guildEntry['experience'] = _newGuildRank['experience'] # type: ignore
#             _guildEntry['level'] = _newGuildRank['level'] # type: ignore

#             _gainedGuildLevels += _newGuildRank['gained']

#     _tmpStr = '{\n'
#     log.DEBUG(f"Gained {_gainedGuildLevels} Guild levels.\nGained {_gainedGlobalLevels} Global levels.\nNew User Data: {str(_userData).replace('{', _tmpStr)}")

#     await updateUser(user, _userData)

# async def updateUserBank(guild: discord.Guild, user: discord.User | discord.Member, amount: float | int = 0, reason: str = "misc", userdata = None):
# log.DEBUG(f"{user} recieved ${amount}")

# _guildData = await retrieveGuild(guild)
# if _guildData is None:
#     return

# # _userData: dict
# if userdata is not None:
#     _userData = userdata
# else:
#     _userData = await retrieveUser(user) # type: ignore

# if _userData is None: # something went wrong
#     return

# if _userData['bot']['blacklisted']: # User should not have gotten here while blacklisted but we check just in case.
#     return

# # update global first

# if reason == "reward":
#     _userData['economy']['balance_rewarded'] += amount
#     _userData['economy']['balance'] += amount

# if reason == "received":
#     _userData['economy']['balance_received'] += amount
#     _userData['economy']['balance'] += amount

# if reason == "payment":
#     _userData['economy']['balance_paid'] += amount
#     _userData['economy']['balance'] -= amount

# if reason == "misc":
#     _userData['economy']['balance_misc'] += amount
#     _userData['economy']['balance'] += amount

# # then guild

# _userGuildAccount: dict = None # type: ignore

# if len(_userData['economy']['guilds']) > 0:
#     for _entry in _userData['economy']['guilds']:
#         if _entry['id'] == guild.id:
#             _userGuildAccount = _entry

# if _guildData['extras']['guild_economy']['enabled']:
#     if _userGuildAccount is None: # Could not find a guild specific economy entry. Create a new one using guild defaults

#         _newAmount = _guildData['extras']['guild_economy']['starting_balance']
#         _userGuildAccount: dict = {
#             'id': guild.id,
#             'balance': _newAmount,
#             'balance_rewarded': 0,
#             'balance_received': 0,
#             'balance_paid': 0,
#             'balance_misc': 0}

#         if reason == "reward":
#             _userGuildAccount['balance'] += amount
#             _userGuildAccount['balance_rewarded'] += amount
#         if reason == "received":
#             _userGuildAccount['balance'] += amount
#             _userGuildAccount['balance_received'] += amount
#         if reason == "payment":
#             _userGuildAccount['balance'] -= amount
#             _userGuildAccount['balance_paid'] += amount
#         if reason == "misc":
#             _userGuildAccount['balance'] += amount
#             _userGuildAccount['balance_misc'] += amount

#         log.DEBUG(f"Creating New Bank Account For {user.name}. \nData:{_userGuildAccount}")
#         _userData['economy']['guilds'].append(_userGuildAccount)
#     else: # Found guild specific economy, Update

#         if reason == "reward":
#             _userGuildAccount['balance'] += amount
#             _userGuildAccount['balance_rewarded'] += amount
#         if reason == "received":
#             _userGuildAccount['balance'] += amount
#             _userGuildAccount['balance_received'] += amount
#         if reason == "payment":
#             _userGuildAccount['balance'] -= amount
#             _userGuildAccount['balance_paid'] += amount
#         if reason == "misc":
#             _userGuildAccount['balance'] += amount
#             _userGuildAccount['balance_misc'] += amount

# if userdata is not None:
#     return _userData

# await updateUser(user, _userData)
