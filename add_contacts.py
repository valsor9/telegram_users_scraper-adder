from telethon import TelegramClient
# from telethon.tl.functions.messages import AddChatUserRequest
# from telethon.tl.types import InputPhoneContact
# from telethon.tl.functions.contacts import ImportContactsRequest
from telethon.tl.functions.contacts import DeleteContactsRequest
from telethon import functions, types
from telethon.errors import FloodWaitError
import json, time
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
# username = config['Telegram']['username']
my_phone = config['Telegram']['phone']

client = TelegramClient(my_phone, api_id, api_hash)
client.flood_sleep_threshold = 24 * 60 * 60
client.start()

async def main():
    #me = await client.get_me()
    with open('channel_users.json', encoding='utf-8') as f:
        j = json.load(f)
        c = 0

        for i, d in enumerate(j):
            if d['is_bot']:
                print("d['is_bot']", d['is_bot'], d)
                continue

            id = d['id']

            phone = ''
            if d['phone']:
                phone = d['phone']

            first = d['first_name']
            if not first:
                first = str(id)

            last = d['last_name']
            if not last:
                last = ''

            try:
                print('Contact:')
                print(d)
                # add user to contact
                # result = await client(functions.contacts.ImportContactsRequest(
                #     contacts=[types.InputPhoneContact(
                #         client_id=0,
                #         phone=phone,
                #         first_name=first,
                #         last_name=last
                #     )]
                # ))
                result = await client(functions.contacts.AddContactRequest(
                    id=id,
                    first_name=first,
                    last_name=last,
                    phone=phone
                ))
                print('Result: ', result.stringify())

                c += 1
                print(f'{c} contacts have been added.')

                slp = 30
                for s in range(slp, 0, -1):
                    print(f'Waiting next contact: {s} seconds')
                    time.sleep(1)

            except FloodWaitError as e:
                print(e)
                sleep_time = range(e.seconds, 0, -1)
                for s in sleep_time:
                    print(f'Remaining sleep time: {s} seconds')
                    time.sleep(1)



with client:
    client.loop.run_until_complete(main())