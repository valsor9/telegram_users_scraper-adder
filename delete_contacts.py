from imports import *

async def main():
    contacts = await client(functions.contacts.GetContactIDsRequest(
        hash=0
    ))

    print('1 - delete all contacts\n2 - delete recent contacts')
    choice = input('Option: ')

    if choice == '1':
        c = 0
        for n, cid in enumerate(contacts):
            result = await client(functions.contacts.DeleteContactsRequest(
                id=[cid]
            ))
            print('Result: ', result.stringify())
            c += 1
        print(f'{c}/{len(contacts)} contacts have been deleted.')
    else:
        with open('channel_users.json', encoding='utf-8') as f:
            j = json.load(f)
            c = 0
            for i, d in enumerate(j):
                for n, cid in enumerate(contacts):
                    if cid == d['id']:
                        print('Contact: ', d)
                        result = await client(functions.contacts.DeleteContactsRequest(
                                        id=[cid]
                                    ))
                        print(result.stringify())
                        c += 1
        print(f'{c}/{len(contacts)} contacts have been deleted.')


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read("config.ini")

    api_id = config['Telegram']['api_id']
    api_hash = config['Telegram']['api_hash']
    # username = config['Telegram']['username']
    my_phone = config['Telegram']['phone']

    client = TelegramClient(my_phone, api_id, api_hash)
    client.start()

    with client:
        client.loop.run_until_complete(main())