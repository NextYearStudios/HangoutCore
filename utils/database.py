class database():
    def __init__(self):
        pass

    # def connect():
    #     if bot.cfg["database"]["type"] == "mysql":
    #         DatabaseConnection = mysql.connector.connect(
    #             database = bot.cfg["database"]["name"],
    #             host = bot.cfg["database"]["host"],
    #             user = bot.cfg["database"]["user"],
    #             password = bot.cfg["database"]["password"],
    #         )

    #         return DatabaseConnection
        
    async def RegisterGuild(loop, guild: discord.Guild):
        pool = await aiomysql.create_pool(
            db = bot.cfg["database"]["name"],
            host = bot.cfg["database"]["host"],
            port = bot.cfg["database"]["port"],
            user = bot.cfg["database"]["user"],
            password = bot.cfg["database"]["password"]

        )


    # async def RegisterGuild(guild: discord.Guild):
    #     async with asqlite.connect(cfg['database']['name']) as conn:
    #         async with conn.cursor() as cursor:
    #             await cursor.execute('''\
    #                 CREATE TABLE IF NOT EXISTS guilds 
    #                 (id integer PRIMARY KEY UNIQUE NOT NULL, name text, guild_notification_channel_id integer, stickymessage_ids text, stickymessage_moderator_id integer, autorole_enabled text NOT NULL DEFAULT 'False', autorole_moderator_id integer, autorole_role_ids text, selfrole_enabled text NOT NULL DEFAULT 'False', selfrole_moderator_id integer, selfrole_role_ids text, guildstats_enabled text NOT NULL DEFAULT 'False', guildstats_channel_id integer, guildstats_options text, voicelobby_enabled text NOT NULL DEFAULT 'False', voicelobby_channel_id integer, guildsuggestions_enabled text NOT NULL DEFAULT 'False', guildsuggestions_channel_id integer, ticketsystem_enabled text NOT NULL DEFAULT 'False', ticketsystem_moderator_id integer, ticketsystem_channel_id integer)''')
    #             await cursor.execute(f"""\
    #                 SELECT * FROM guilds 
    #                 WHERE id = (?)
    #                 """,(guild.id))
    #             result = await cursor.fetchone()
    #             if result is None:
    #                 await cursor.execute(f"""\
    #                     INSERT INTO guilds
    #                     (id, name, autorole_enabled, selfrole_enabled, guildstats_enabled, voicelobby_enabled, guildsuggestions_enabled, ticketsystem_enabled)
    #                     VALUES( ?, ?, 'False', 'False', 'False', 'False', 'False', 'False')
    #                     """, (guild.id, guild.name))
    #                 await conn.commit()
    #             else:
    #                 await cursor.execute(f"""\
    #                     UPDATE guilds SET name = ?
    #                     WHERE id = ?"""
    #                     , (guild.name, guild.id))

    # async def RegisterGuildNotificationChannel(guild: discord.Guild, channel: discord.TextChannel):
    #     async with asqlite.connect(cfg['database']['name']) as conn:
    #         async with conn.cursor() as cursor:
    #             if channel is not None:
    #                 await cursor.execute(f"""\
    #                     UPDATE guilds SET guild_notification_channel_id = ?
    #                     WHERE id = ?
    #                     """, (channel.id, guild.id))
                
    #             await conn.commit()
    
    # async def RetrieveGuildNotificationChannel(guild: discord.Guild):
    #     async with asqlite.connect(cfg['database']['name']) as conn:
    #         async with conn.cursor() as cursor:
    #             await cursor.execute(f"""SELECT guild_notification_channel_id FROM guilds WHERE id = ?""", (guild.id))
    #             result = await cursor.fetchall()
    #             if result is not None:
    #                 if result[0][0] is not None:
    #                     NotificationChannel = discord.utils.get(guild.channels, id=result[0][0])
    #                     return NotificationChannel
    #                 else:
    #                     return None

    # async def RegisterAutoRoleSystem(guild: discord.Guild, enabled: bool = None, moderator_role: discord.Role = None, role_ids: list[int] = None):
    #     async with asqlite.connect(cfg['database']['name']) as conn:
    #         async with conn.cursor() as cursor:
    #             if enabled is not None:
    #                 await cursor.execute(f"""\
    #                     UPDATE guilds SET autorole_enabled = ?
    #                     WHERE id = ?
    #                     """, (enabled, guild.id))
    #             if moderator_role is not None:
    #                 await cursor.execute(f"""\
    #                     UPDATE guilds SET autorole_moderator_id = ?
    #                     WHERE id = ?
    #                     """, (moderator_role.id, guild.id))
    #             if role_ids is not None:
    #                 await cursor.execute(f"""\
    #                     UPDATE guilds SET autorole_role_ids = ?
    #                     WHERE id = ?
    #                     """, (role_ids, guild.id))
    #             await conn.commit()

    # async def RetrieveAutoRoleSystem(guild: discord.Guild):
    #     async with asqlite.connect(cfg['database']['name']) as conn:
    #         async with conn.cursor() as cursor:
    #             await cursor.execute(f"""SELECT autorole_enabled, autorole_moderator_id, autorole_role_ids FROM guilds WHERE id = ?""", (guild.id))
    #             result = await cursor.fetchall()
    #             if result is not None:
    #                 return result[0]

    # async def RegisterTicketSystem(guild: discord.Guild, enabled: bool = None, category_id: discord.CategoryChannel = None, moderator_role: discord.Role = None):
    #     async with asqlite.connect(cfg['database']['name']) as conn:
    #         async with conn.cursor() as cursor:
    #             if enabled is not None:
    #                 await cursor.execute(f"""\
    #                     UPDATE guilds SET ticketsystem_enabled = ?
    #                     WHERE id = ?
    #                     """, (enabled, guild.id))
                
    #             if category_id is not None:
    #                 await cursor.execute(f"""\
    #                     UPDATE guilds SET ticketsystem_channel_id = ?
    #                     WHERE id = ?
    #                     """, (category_id.id, guild.id))
                
    #             if moderator_role is not None:
    #                 await cursor.execute(f"""\
    #                     UPDATE guilds SET ticketsystem_moderator_id = ?
    #                     WHERE id = ?
    #                     """, (moderator_role.id, guild.id))
    #             await conn.commit()

    # async def RetrieveTicketSystem(guild: discord.Guild):
    #     async with asqlite.connect(cfg['database']['name']) as conn:
    #         async with conn.cursor() as cursor:
    #             await cursor.execute(f"""SELECT ticketsystem_enabled, ticketsystem_channel_id, ticketsystem_moderator_id FROM guilds WHERE id = ?""", (guild.id))
    #             result = await cursor.fetchall()
    #             if result is not None:
    #                 return result[0]
