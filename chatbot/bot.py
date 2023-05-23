from twitchAPI import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.types import AuthScope, ChatEvent
from twitchAPI.chat import Chat, EventData, ChatMessage, ChatSub, ChatCommand
import os
from dotenv import load_dotenv
from pathlib import Path
import asyncio
import sqlite3
from sqlite3 import Error
from time import gmtime, strftime
import re

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

APP_ID = os.getenv('TWITCH_CLIENT_ID')
APP_SECRET = os.getenv('TWITCH_SECRET')
USER_SCOPE = [AuthScope.CHAT_READ]
TARGET_CHANNEL = 'ruetoo'

garf_regex = r'\.*garf\.*'
jiggler_regex = r'\.*jiggl\.*'

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        global conn 
        conn = sqlite3.connect(db_file, check_same_thread=False)
        print('DB Connection success')
    except Error as e:
        print(e)

def main():
    database = '../db/database'
    create_connection(database)

def get_current_time():
    return strftime("%Y-%m-%d %H:%M:%S", gmtime())

def make_user_if_not_exists(username):
    if conn is not None:
        cur = conn.cursor()
        cur.execute("SELECT * FROM user WHERE name = ?", (username,))

        result = cur.fetchall()

        if len(result) == 0:
            sql = '''INSERT INTO user(name) VALUES (?)'''
            cur = conn.cursor()
            cur.execute(sql, (username, ))
            conn.commit()
    else:
        print("Error! cannot create the database connection.")
    
def get_user_id(username):
    if conn is not None:
        cur = conn.cursor()
        cur.execute("SELECT id FROM user WHERE name = ?", (username, ))
        
        result = cur.fetchall()
        
        return result[0][0]

def add_jiggler(username):
    if conn is not None:
        make_user_if_not_exists(username)
        id = get_user_id(username)
        print(id, username)
        
        sql = '''INSERT INTO message(jiggle, date, user_id) VALUES (?, ?, ?)'''

        cur = conn.cursor()
        cur.execute(sql, (1, get_current_time(), id))
        conn.commit()

    else:
        print("Error! cannot create the database connection.")

def add_garfer(username):
    if conn is not None:
        make_user_if_not_exists(username)
        id = get_user_id(username)
        print(id, username)
        
        sql = '''INSERT INTO message(jiggle, date, user_id) VALUES (?, ?, ?)'''

        cur = conn.cursor()
        cur.execute(sql, (0, get_current_time(), id))
        conn.commit()


    else:
        print("Error! cannot create the database connection.")


# this will be called when the event READY is triggered, which will be on bot start
async def on_ready(ready_event: EventData):
    print('Bot is ready for work, joining channels')
    # join our target channel, if you want to join multiple, either call join for each individually
    # or even better pass a list of channels as the argument
    await ready_event.chat.join_room(TARGET_CHANNEL)
    # you can do other bot initialization things in here


# this will be called whenever a message in a channel was send by either the bot OR another user
async def on_message(msg: ChatMessage):
    user = msg.user.name
    if re.search(jiggler_regex, msg.text, flags=re.IGNORECASE):
        print(f'Jiggler detected: {user}')
        add_jiggler(user)
    if re.search(garf_regex, msg.text, flags=re.IGNORECASE):
        print(f'Garfer detected: {user}')
        add_garfer(user)

# this is where we set up the bot
async def run():
    # set up twitch api instance and add user authentication with some scopes
    twitch = await Twitch(APP_ID, APP_SECRET)
    auth = UserAuthenticator(twitch, USER_SCOPE)
    token, refresh_token = await auth.authenticate()
    await twitch.set_user_authentication(token, USER_SCOPE, refresh_token)

    # create chat instance
    chat = await Chat(twitch)

    # register the handlers for the events you want

    # listen to when the bot is done starting up and ready to join channels
    chat.register_event(ChatEvent.READY, on_ready)
    # listen to chat messages
    chat.register_event(ChatEvent.MESSAGE, on_message)
    # listen to channel subscriptions


    # we are done with our setup, lets start this bot up!
    chat.start()

    # lets run till we press enter in the console
    try:
        input('press ENTER to stop\\n')
    finally:
        # now we can close the chat bot and the twitch api client
        chat.stop()
        await twitch.close()



if __name__ == '__main__':
    main()

# lets run our setup
asyncio.run(run())
