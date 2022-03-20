''' REPO MODULES '''
from baobapp.utils import json_items_from_file, make_base64_qr_code, get_kivy_image_from_bytes
from baobapp.models.sharedata.decentralized_share_link import DecentralizedShareLink
from baobapp.models.sharedata.statements.statement_contact_link import StatementContactLink
from baobapp.models.process.data_actions import DataActions
from kivy.lang import Builder

''' KIVY MODULES '''
from kivy.uix.label import Label
from kivy.properties import StringProperty
from kivy.clock import Clock

''' KIVYMD MODULES '''
from kivymd.uix.list import OneLineListItem, TwoLineAvatarListItem, ThreeLineListItem, IconLeftWidget, ImageLeftWidget, OneLineAvatarListItem, ThreeLineListItem
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFloatingActionButton, MDRoundFlatIconButton, MDFillRoundFlatButton, MDRectangleFlatIconButton, MDRoundFlatButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.card import MDCard
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.toast import toast
from kivy.core.clipboard import Clipboard

''' OTHERS '''
import json
import time
import requests
from os import listdir, path, unlink, makedirs, remove
from threading import Thread
import json
from functools import partial
from datetime import datetime, timedelta
from base64 import b64decode, b64encode
import multiprocessing
from kivy_garden.zbarcam import ZBarCam
from kivymd.uix.swiper import MDSwiper, MDSwiperItem
from baobapp.models.exeptions import NoInternetConnection
from baobapp.socket_listeners import get_all_sockets, disconnect_all_accounts

''' OWNNETORWKAPI MODULES '''
from ownnetwork.baobap.file_management import ManagementFile

WIDGET_BUILDER_PATH = 'baobapp/screens/home/widgets/'

class ContentJsonCodeDialog(MDBoxLayout):
    input_text = StringProperty()

    def on_text_validate(self, input_text: dict):
        toast(input_text, type(input_text))

Builder.load_file(WIDGET_BUILDER_PATH + 'swiperavatarqrcode.kv')

class SwiperAvatarQrCode(MDSwiperItem):
    surname = StringProperty()
    qrcodedata = StringProperty()

#

Builder.load_file(WIDGET_BUILDER_PATH + 'contentaccountinformation.kv')

class ContectAccountInformation(MDBoxLayout):
    qrcodedata = StringProperty()

    def DecentralizedLink(self, qrcodedata):
        try:
            link = DecentralizedShareLink(qrcodedata)
            toast('The link is being generated, the application is freezing, please waiting')
            Clipboard.copy(link)
        except NoInternetConnection:
            toast('You don''t have internet connection')
            return

Builder.load_file(WIDGET_BUILDER_PATH + 'dialogaddingaccount.kv')
class DialogAddingAccount(MDBoxLayout):

    def on_text_validate(self, input_text: str):
        host, port = input_text.split(':')
        DataActions().adding_account(host, int(port))

class AccountItemSource(OneLineAvatarListItem):
    divider = None
    source = StringProperty()
    text = StringProperty()

class AccountItemIcon(OneLineAvatarListItem):
    divider = None
    icon = StringProperty()

class AccountCard(MDCard):
    caption = StringProperty()
    source = StringProperty()

class Content(MDBoxLayout):
    '''Custom content.'''

class HomeScreen(MDScreen):

        # TODO: Action button from frame menu
    FrameMenu_FloatingActionButton = {
            'Add user-id': 'qrcode-scan'
    }

    dialog_error = None
    dialog = None
    jsoncode_dialog = None
    urllink_dialog = None
    public_host_dialog = None

    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)

        self.accountinformation_dialog = None
        self.dialog_adding_account = None
        self.mf = ManagementFile()


    def conv_inactive_list_builder(self):
        self.ids.message_conv_list.clear_widgets()

        self.manager.chatscreen.read_recv_data(1)
        new_read_conv_content = self.manager.chatscreen.new_read_conv_content

        new_conv_list = []
        conv_list = []

        for key, value in json_items_from_file('db/users.json'):
            if new_read_conv_content.get(key):
                new_conv_list.append({'id': key, 'name': value['surname'], 'lastmessage': new_read_conv_content[key][-1]['data']})
            
            elif not new_read_conv_content.get(key):
                conv_list.append({'id': key, 'name': value['surname']})

        ''' New conversation list '''
        availablelabel = MDLabel(text = 'You have new message(s)!', halign = "center", theme_text_color = "Custom", text_color = (76, 235, 139, 1), parent_background = (48, 48, 48, 1))
        noavailablelabel = MDLabel(text = 'You have not received new message(s) ...', halign = "center", theme_text_color = "Custom", text_color = (235, 76, 76, 1), parent_background = (48, 48, 48, 1))

        if new_conv_list:
            self.ids.message_conv_list.add_widget(availablelabel)
            
            for value in new_conv_list:
                avatar = ImageLeftWidget(source=self.mf.avatar_from_user_id_exist("user", value['id']))
                items = TwoLineAvatarListItem(text='[color=#222222]' + value['name'], secondary_text='[color=#8D8E90]' + value['lastmessage'], on_release=lambda x, id=value['id']: self.c.change_screen('chat', id))
                items.add_widget(avatar)
                
                self.ids.message_conv_list.add_widget(items)
        
        elif not new_conv_list:
            self.ids.message_conv_list.add_widget(noavailablelabel)

        ''' Others conversations list '''
        for value in conv_list:
            avatar = ImageLeftWidget(source = self.mf.avatar_from_user_id_exist("user", value['id']))
            items = TwoLineAvatarListItem(text= '[color=#222222]' + value['name'], secondary_text = '[color=#8D8E90]ID : ' + value['id'][-8:] + '...', on_release = lambda x, id = value['id']: self.manager.change_screen('chat', id))
            items.add_widget(avatar)
            
            self.ids.message_conv_list.add_widget(items)

    def reload_hosts_info(self):

        socket_list = self.manager.chatscreen.socket_list

        disconnect_all_accounts(socket_list)
        self.manager.chatscreen.socket_list = get_all_sockets()

        socket_list = self.manager.chatscreen.socket_list
        serverlist = self.mf.file_hostinfo(socket_list)

        with open('db/hosts.json', 'w+') as file:
            json.dump(serverlist, file)

        return serverlist, socket_list

    def relaod_public_host_dialog(self):
        self.public_host_dialog.dismiss()
        self.public_host_dialog = None
        self.show_public_host_dialog()
        toast('Please no spamming this')

    def show_public_host_dialog(self):
        if not self.public_host_dialog:

            serverlist, socket_list = self.reload_hosts_info()
            box_items = []
            test = 'test'

            for key, value in serverlist.items():

                avatar = ImageLeftWidget(source = f"db/img/hosts/node/{key}.png")
                server = key
                item = TwoLineAvatarListItem(text= '[color=#222222]' + value['name'], secondary_text = '[color=#8D8E90]Statut : ' + str(value['statut']), on_release = lambda x, key = key: print(key))
                item.add_widget(avatar)

                box_items.append(item)
            
            icon_account_plus = IconLeftWidget(icon="account-plus")
            item = OneLineAvatarListItem(text = '[color=#222222]' + 'Adding host', on_release = lambda x, test = test: print(test))
            item.add_widget(icon_account_plus)

            box_items.append(item)

            icon_reload = IconLeftWidget(icon="reload")
            item = OneLineAvatarListItem(text = '[color=#222222]' + "Reload host informations", on_release = lambda x, test = test: self.relaod_public_host_dialog())
            item.add_widget(icon_reload)
            
            box_items.append(item)

            self.public_host_dialog = MDDialog(
                title="Public-host list :",
                type="simple",
                items=box_items
                )
        
        self.public_host_dialog.open()

    def show_account_dialog(self):
        if not self.account_list_dialog:

            items = []
            
            for key, value in json_items_from_file('db/accounts.json'):
                items.append(AccountItemSource(text=key, source=self.mf.avatar_from_user_id_exist("account", key)))
                items.append(AccountItemIcon(text="Add account", icon="account-plus"))

            self.account_list_dialog = MDDialog(
                title="Accounts",
                type="simple",
                items=items
                )

        self.account_list_dialog.open()

    def automatic_adding_contact(self):

        try:
            url_clipboard = Clipboard.paste()
            
            if url_clipboard.startswith('{') and url_clipboard.endswith('}'):
                DataActions().adding_contact(json.loads(url_clipboard.replace("'", '"')))
            
            elif not url_clipboard.startswith('{').endswith('}'):
                
                valid_link = StatementContactLink(url_clipboard)
                
                if valid_link:
                    DataActions().adding_contact(valid_link)
                elif not valid_link:
                    toast('No valid link')
        
        except Exception as e:
            toast(str(e))
            raise

    def automatic_adding_account(self):

        DataActions().adding_account("", 8080)

    def callback_for_menu_items(self, *args):
        if args[0] == "Qr Code":
            print('Json code')
        elif args[0] == "Json code":
            print('Json code')
            self.show_jsoncode_dialog()
        elif args[0] == "Bluetooth":
            print('Bluetooth')
        elif args[0] == "Link URL":
            self.show_urllink_dialog()

    def dialog_adding_accounts(self):

        self.dialog_adding_account = MDDialog(
                title="Adding account",
                type="custom",
                content_cls= DialogAddingAccount()
        )

        self.dialog_adding_account.open()

    def show_accounts_informations(self, value: dict, key: str):
        qrcodedata = {
                      "host": value['host'],
                      "port": value['port'],
                      "id": key,
                      "public_key": b64encode(value['public_key'].encode()).decode(),
                      "type_crypto": value['type_crypto']
                      }

        self.accountinformation_dialog = MDDialog(
                title=key,
                type="custom",
                content_cls= ContectAccountInformation(qrcodedata = str(qrcodedata))
        )
        self.accountinformation_dialog.open()

    def accounts_lists(self):
        self.ids.my_accounts.clear_widgets()

        with open('db/hosts.json', 'r') as file:
            hosts = json.load(file)

        for key, value in json_items_from_file('db/accounts.json'):

            host_and_port = value['host'] + '_' + str(value['port'])

            avatar = ImageLeftWidget(source=self.mf.avatar_from_user_id_exist("account", key))
            items = TwoLineAvatarListItem(text='[color=#222222]' + key, secondary_text='[color=#8D8E90]from ' + hosts[host_and_port]['name'], on_release=lambda x, account_id=key, account_value=value: self.show_accounts_informations(account_value, account_id))
            items.add_widget(avatar)
            self.ids.my_accounts.add_widget(items)

    def add_(self):
        bottom_sheet_menu = MDGridBottomSheet()
        data = {
            "Qr Code": "qrcode-scan",
            "Json code": "code-json",
            "Link URL": "link",
            "Bluetooth": "bluetooth"
        }
        for item in data.items():
            bottom_sheet_menu.add_item(
                item[0],
                lambda x, y=item[0]: self.callback_for_menu_items(y),
                icon_src=item[1],
            )
        #bottom_sheet_menu.open()

    #def show_swiper_account(self):
    #    self.ids.user_list_nav.clear_widgets()
    #    for key, value in json_items_from_file('db/accounts.json'):

    #        qrcodedata = {
    #                      'host': value['host'],
    #                      'port': value['port'],
    #                      'id': key,
    #                      'public_key': value['public_key'],
    #                      'type_crypto': value['type_crypto']
    #                      }
    #        print('loop', key)
    #        self.ids.user_list_nav.add_widget(SwiperAvatarQrCode(qrcodedata = get_kivy_image_from_bytes(make_base64_qr_code(str(qrcodedata))) , surname= key))

    def show_example_grid_bottom_sheet(self):
        bottom_sheet_menu = MDGridBottomSheet()
        data = {
            "Qr Code": "qrcode-scan",
            "Json code": "code-json",
            "Link URL": "link",
            "Bluetooth": "bluetooth"
        }
        for item in data.items():
            bottom_sheet_menu.add_item(
                item[0],
                lambda x, y=item[0]: self.callback_for_menu_items(y),
                icon_src=item[1],
            )
        #bottom_sheet_menu.open()
