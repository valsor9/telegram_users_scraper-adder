from telethon.sync import TelegramClient
from telethon import functions, types
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError, UserNotMutualContactError
from telethon.tl.functions.channels import InviteToChannelRequest
import traceback
import time
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
# username = config['Telegram']['username']
my_phone = config['Telegram']['phone']

client = TelegramClient(my_phone, api_id, api_hash)
client.start()

async def main():
    chats = []
    last_date = None
    chunk_size = 200
    groups = []

    res = await client(GetDialogsRequest(
        offset_date=last_date,
        offset_id=0,
        offset_peer=InputPeerEmpty(),
        limit=chunk_size,
        hash=0
    ))
    chats.extend(res.chats)

    for chat in chats:
        try:
            if chat.megagroup == True:
                groups.append(chat)
        except:
            continue

    print('Choose a group to add members:')
    i = 0
    for g in groups:
        print(str(i) + ' - ' + g.title)
        i += 1

    g_index = input('Enter a number: ')
    target_group = groups[int(g_index)]
    target_group_entity = InputPeerChannel(target_group.id, target_group.access_hash)

    result = await client(functions.contacts.GetContactIDsRequest(
        hash=0
    ))

    n = 0
    for id in result:
        n += 1
        if n % 51 == 0:
            print('50 users have been added\nWaiting 15 minutes...')
            time.sleep(900)
            # for s in range(900, 0, -1):
            #     print(f'Remaining time: {s} seconds')
            #     time.sleep(1)
        print(f'Contact id: {id}')
        contact_entity = await client.get_entity(id)
        acs_hash = contact_entity.access_hash
        print(f'Contact access hash: {acs_hash}')

        try:
            print(f"Adding contact...")
            user_to_add = InputPeerUser(id, acs_hash)

            r = await client(InviteToChannelRequest(target_group_entity, [user_to_add]))
            print(r)

            # print("Waiting 60 Seconds...")
            # time.sleep(60)

        except PeerFloodError:
            print("Getting Flood Error from telegram. Script is stopping now. Please try again after some time.")
        except UserPrivacyRestrictedError:
            print("The user's privacy settings do not allow you to do this.\nSkipping...")
            continue
        except UserNotMutualContactError:
            print('The provided user is not a mutual contact.')
        except:
            traceback.print_exc()
            print("Unexpected Error")
            continue

with client:
    client.loop.run_until_complete(main())