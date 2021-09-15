    # graber
import configparser
#import json
from telethon.sync import TelegramClient
from telethon import connection
from datetime import date, datetime
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from telethon.tl.functions.messages import GetHistoryRequest

    # add_contacts
#from telethon import TelegramClient
# from telethon.tl.functions.messages import AddChatUserRequest
# from telethon.tl.types import InputPhoneContact
# from telethon.tl.functions.contacts import ImportContactsRequest
from telethon.tl.functions.contacts import DeleteContactsRequest
from telethon import functions, types
from telethon.errors import FloodWaitError
import json, time

    # add_to_group
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser, InputChannel
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError, UserNotMutualContactError
from telethon.tl.functions.channels import InviteToChannelRequest
import traceback
#import time