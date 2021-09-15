from imports import *

async def get_group():
	chats = []
	last_date = None
	chunk_size = 200
	groups = []

	res = await client(functions.messages.GetDialogsRequest(
		offset_date=last_date,
		offset_id=0,
		offset_peer=InputPeerEmpty(),
		limit=chunk_size,
		hash=0
	))
	chats.extend(res.chats)

	for chat in chats:
		try:
			if chat.megagroup:
				groups.append(chat)
		except:
			continue

	print('\nChoose a group:')
	i = 0
	for g in groups:
		print(str(i) + ' - ' + g.title)
		i += 1

	g_index = input('Enter group\'s number: ')
	print()
	target_group = groups[int(g_index)]
	target_group_entity = InputChannel(target_group.id, target_group.access_hash)

	return target_group_entity


async def dump_all_participants(channel):
	offset_user = 0
	limit_user = 100

	all_participants = []
	filter_user = ChannelParticipantsSearch('')

	while True:
		participants = await client(GetParticipantsRequest(channel,
			filter_user, offset_user, limit_user, hash=0))
		if not participants.users:
			break
		all_participants.extend(participants.users)
		offset_user += len(participants.users)

	all_users_details = []

	me = await client.get_me()
	for participant in all_participants:
		if participant.id != me.id:
			all_users_details.append({"id": participant.id,
				"first_name": participant.first_name,
				"last_name": participant.last_name,
				"user": participant.username,
				"phone": participant.phone,
				"is_bot": participant.bot})

	with open('channel_users.json', 'w', encoding='utf8') as outfile:
		json.dump(all_users_details, outfile, ensure_ascii=False, indent=4)


async def add_contacts():
	with open('channel_users.json', encoding='utf-8') as f:
		j = json.load(f)
		c = 0
		for i, d in enumerate(j):
			if d['is_bot']:
				print("BOT: ", d['is_bot'], d)
				print()
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
				print('Contact: ', d)
				result = await client(functions.contacts.AddContactRequest(
					id=id,
					first_name=first,
					last_name=last,
					phone=phone
				))
				print('Result: ', result.stringify())

				c += 1
				print(f'{c} contacts have been added.')
				print()

				if i != len(j)-1:
					slp = 30
					for s in range(slp, 0, -1):
						print(f'Waiting next contact: {s} seconds', end='\r')
						time.sleep(1)

			except FloodWaitError as e:
				print(e)
				sleep_time = range(e.seconds, 0, -1)
				for s in sleep_time:
					print(f'Remaining sleep time: {s} seconds', end='\r')
					time.sleep(1)



async def add_to_group(target_group_entity):
	cntcts = await client(functions.contacts.GetContactIDsRequest(
		hash=0
	))
	with open('channel_users.json', encoding='utf-8') as f:
		jsn = json.load(f)
		n = 0
		c = 0
		for i, id in enumerate(cntcts):
			for j, usr in enumerate(jsn):
				if id == usr['id']:
					n += 1
					if i != len(cntcts)-1:
						if n % 51 == 0:
							print(f'{c}/{len(cntcts)} users have been added.\nNeed to wait 15 minutes to continue.')
							# time.sleep(900)
							for s in range(900, 0, -1):
								print(f'Remaining time: {s} seconds', end='\r')
								time.sleep(1)

					print(f'Contact id: {id}')
					contact_entity = await client.get_entity(id)
					acs_hash = contact_entity.access_hash
					print(f'Contact access hash: {acs_hash}')

					try:
						print(f"Adding contact to the group...")
						user_to_add = InputPeerUser(id, acs_hash)

						r = await client(InviteToChannelRequest(target_group_entity, [user_to_add]))
						print('Result: ', r.stringify())
						c += 1
						print(f'{c}/{len(cntcts)} recent contacts have been added to the group.')

						if i != len(cntcts) - 1:
							slp = 60
							for s in range(slp, 0, -1):
								print(f'Waiting {s} seconds...', end='\r')
								time.sleep(1)

					except FloodWaitError as e:
						print(e)
						sleep_time = range(e.seconds, 0, -1)
						for s in sleep_time:
							print(f'Remaining sleep time: {s} seconds', end='\r')
							time.sleep(1)
					except UserPrivacyRestrictedError:
						print("The user's privacy settings do not allow you to do this. Skipping...")
					except UserNotMutualContactError:
						print('The provided user is not a mutual contact. Skipping...')
					except:
						traceback.print_exc()
						print("Unexpected Error.")


async def main():
	print('Choose group for fetching users:\n1 - by link\n2 - from list')
	choice = input('Type number: ')
	if choice == '1':
		url = input("Insert link: ")
		from_group = await client.get_input_entity(url)
	else:
		from_group = await get_group()

	print('\nChoose group for adding users:\n1 - by link\n2 - from list')
	choice = input('Type number: ')
	if choice == '1':
		url = input("Insert link: ")
		to_group = await client.get_input_entity(url)
	else:
		to_group = await get_group()

	await dump_all_participants(from_group)
	await add_contacts()
	await add_to_group(to_group)


if __name__ == '__main__':
	config = configparser.ConfigParser()
	config.read("config.ini")

	api_id = config['Telegram']['api_id']
	api_hash = config['Telegram']['api_hash']
	# username = config['Telegram']['username']
	my_phone = config['Telegram']['phone']

	client = TelegramClient(my_phone, api_id, api_hash)
	client.flood_sleep_threshold = 24 * 60 * 60
	client.start()

	with client:
		client.loop.run_until_complete(main())