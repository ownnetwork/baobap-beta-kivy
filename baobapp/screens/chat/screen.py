''' REPO MODULES '''
from baobapp.utils import json_items_from_file

''' KIVY MODULES '''
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.properties import StringProperty
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty

''' KIVYMD MODULES '''
from kivymd.uix.imagelist import SmartTileWithLabel
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFloatingActionButton, MDRoundFlatIconButton, MDFillRoundFlatButton, MDRectangleFlatIconButton, MDRoundFlatButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.card import MDCard
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.icon_definitions import md_icons
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.bottomsheet import MDGridBottomSheet, MDListBottomSheet
from kivymd.toast import toast

''' OWNNETORWKAPI MODULES '''
from ownnetwork.baobap.api import NodeHostAPI
from ownnetwork.baobap.file_management import ManagementFile
from ownnetwork.baobap.models.crypto.universal import UNIVERSALCrypto
from ownnetwork.baobap.models.chat.add_chat_content import AddChatContent
from ownnetwork.baobap.models.chat.delete_chat_content import DeleteChatContent
from ownnetwork.baobap.models.contact.delete_contact import DeleteContact
from ownnetwork.baobap.models.utils.json_modifier import JsonModifier

''' OTHERS '''
import json
from os import listdir, path, unlink, makedirs, remove
from threading import Thread
import json
from datetime import datetime, timedelta
from base64 import b64decode
import plyer
from datetime import datetime

class SmoothLabel(MDLabel):
    def on_size(self, *args):
        self.text_size = self.size

class SmoothLabelMy(MDLabel):
    def on_size(self, *args):
        self.text_size = self.size

class ChatScreen(MDScreen):

    def __init__(self, socket_list, **kwargs):
        super(ChatScreen, self).__init__(**kwargs)
        
        self.mf = ManagementFile()
        self.new_read_conv_content = {}
        self.socket_list = socket_list
       
        self.dialog_error = None
        self.dialog_id_information = None
    
    def threading_recv_data(self, key, value):
        if value['statut']:
            d = value["server"].async_get_data('get-data')
            
            if d:
                data = json.loads(UNIVERSALCrypto().decrypt_data(value["prv"], b64decode(d['get-data'].encode())))

                plyer.notification.notify(title=SURNAME, message=data['message'], app_icon = 'db/img/logo.jpg')
                    
                if d['from_id'] == USER_ID:
                    chat_id = self.mf.chat_id_from_user_id(d['from_id'])
                    AddChatContent(chat_id, d['from_id'], 'message', data['message'])
                    self.append_roundedlabel_message(d['from_id'], "message", data['message'])
                    
                elif d['from_id'] != USER_ID:
                    self.adding_new_cache_message(d['from_id'], 'message', data['message'])


    def read_recv_data(self, dt):

        for key, value in self.socket_list.items():
            Thread(self.threading_recv_data(key, value)).start()

    def adding_new_cache_message(self, from_id: str, type_msg: str, message: str):
        now = datetime.now()
        year, month, day, hour, minute, second = str(now.year), str(now.month), str(now.day), str(now.hour), str(now.minute), str(now.second)

        if not self.new_read_conv_content.get(from_id):
            self.new_read_conv_content.update({from_id: [{'time': [year, month, day, hour, minute, second],'type': 'message', 'data': message}]})
        elif self.new_read_conv_content.get(from_id):
            self.new_read_conv_content[from_id].append({'time': [year, month, day, hour, minute, second],'type': 'message', 'data': message})


    def append_roundedlabel_message(self, from_id, type, msg):
        
        if type == 'message':

            if from_id == "me":
                label = SmoothLabelMy(text = f"{msg}")
                self.ids.container_chat_content.add_widget(label)

            else:
                label = SmoothLabel(text = f"{msg}")
                self.ids.container_chat_content.add_widget(label)

    def check_data_chat_list(self, year, month, day):
        if not d.get(year):
            d.update({year: {}})
            d = d.copy()

        if not d[year].get(month):
            d[year].update({month: {}})
            d = d.copy()

        if not d[year][month].get(day):
            d[year][month].update({day: {}})
            d = d.copy()

        if d[year][month][day]:
            LabelDate = MDLabel(text = f"{month}/{day}", halign = "center", theme_text_color = "Custom", text_color = (48, 48, 48, 1), parent_background = (48, 48, 48, 1))
            self.ids.container_chat_content.add_widget(LabelDate)

        for inday in d[year][month][day]:
            from_id, type, message = d[year][month][day][inday]['from_id'], d[year][month][day][inday]['type'], d[year][month][day][inday]['data']
            self.append_roundedlabel_message(from_id, type, message)

    def append_new_message(self, year, month, day):
        if not d.get(year):
            d.update({year: {}})
            d = d.copy()

        if not d[year].get(month):
            d[year].update({month: {}})
            d = d.copy()

        if not d[year][month].get(day):
            d[year][month].update({day: {}})
            d = d.copy()

    def send_message(self):

        if not self.ids.input_chat_text.text == "Loading...":
            sendata = self.ids.input_chat_text.text
            self.ids.input_chat_text.text = "Loading..."

            with open("db/users.json", 'r') as f:
                data_file = json.load(f)
                sender_id = data_file[USER_ID]['sender_id']
                public_key = data_file[USER_ID]['public_key']

            try:
                self.socket_list[sender_id]['server'].message(USER_ID, sendata, public_key)
            except:
                self.error_dialog()
                self.ids.input_chat_text.text = ""
                return

            AddChatContent(self.mf.chat_id_from_user_id(USER_ID), "me", 'message', sendata)
            label = SmoothLabelMy(text=f"{sendata}")
            self.ids.container_chat_content.add_widget(label)

            self.ids.input_chat_text.text = ""
            toast("The message was well sent!")

    def error_dialog(self):
        if not self.dialog_error:
            self.dialog_error = MDDialog(
                text="Oops ! The transmission host of your contact person is offline!",
                radius=[20, 7, 20, 7]
            )
        self.dialog_error.open()

    def id_information_dialog(self):
        
        with open("db/users.json", 'r') as f:
            data_file = json.load(f)
            sender_id = data_file[USER_ID]['sender_id']
            host_with_port = data_file[USER_ID]['host'] + ":" + str(data_file[USER_ID]['port'])
            public_key = str(data_file[USER_ID]['public_key'])
            surname = data_file[USER_ID]['surname']

        self.dialog_id_information = MDDialog(
                text=fr"""Sender id : {sender_id} 
Host and port : {host_with_port} 
surname id : {surname} 
public-key hashing : 
{public_key}""",
                radius=[20, 7, 20, 7]
        )
       
        self.dialog_id_information.open()

    def callback_user_grid_cog(self, text):
        self.user_grid_cog.dismiss()

        if text == "Share on json":
            print('Soon...')
        
        elif text == "View information":
            self.show_user_info_grid()

        elif text == "Delete conversation":
            DeleteChatContent(CHAT_ID)
            self.manager.change_screen('home')
            self.change_screen_to_start_chat(USER_ID)
            toast(f'Contact {USER_ID} chat is deleted !')
        
        elif text == "Delete contact":
            DeleteChatContent(CHAT_ID)
            DeleteContact(USER_ID)
            self.manager.change_screen('home')
            toast(f'Contact {USER_ID} is delete !')

    def show_user_info_grid(self):
        if self.user_info_grid:
            self.user_info_grid.dismiss()

        self.user_info_grid = MDListBottomSheet()
            
        with open("db/users.json", 'r') as f:
            data_file = json.load(f)
            sender_id = data_file[USER_ID]['sender_id']
            host_and_port = data_file[USER_ID]['host'] + ":" + str(data_file[USER_ID]['port'])
            public_key = str(data_file[USER_ID]['public_key'])
            surname = data_file[USER_ID]['surname']
            
        data = {
                "tag": surname,
                "send": sender_id,
                "server": host_and_port,
                "shield-key": public_key,
        }
            
        for item in data.items():
            self.user_info_grid.add_item(
                str(item[1]), 
                lambda x, item=item: toast(item[1]),
                icon = item[0]
            )
            
        self.user_info_grid.open()
    
    def show_user_grid_cog(self):
        self.user_grid_cog = MDGridBottomSheet(radius = 10, radius_from = "top", animation= True)
            
        data = {
                "Share on json": "link-box-outline",
                "View information": "account-key",
                "Delete conversation": "delete",
                "Delete contact": "delete"
        }
            
        for item in data.items():
            self.user_grid_cog.add_item(
                item[0],
                lambda x, y=item[0]: self.callback_user_grid_cog(y),
                icon_src=item[1],
            )
            
        self.user_grid_cog.open()

    def change_screen_to_start_chat(self, user_id: str):
        
        global USER_ID
        USER_ID = user_id
        JsonModifier("db/users").rename(user_id, "surname", "Surname")

        with open("db/users.json", 'r') as f:
            data_file = json.load(f)
            surname = data_file[user_id]['surname']
        self.ids.toolbar_chat_screen.title = surname
        global SURNAME
        SURNAME = surname

        global CHAT_ID
        chat_id = self.mf.chat_id_from_user_id(user_id)
        CHAT_ID = chat_id

        self.user_grid_cog = None
        self.user_info_grid = None

        with open(f"db/chat/{chat_id}.json", 'r+') as f:
            d = json.load(f)
            now = datetime.now() + timedelta(days=-9)

            for date in range(10):
                year, month, day = str(now.year), str(now.month), str(now.day)

                if not d.get(year):
                    d.update({year: {}})
                    d = d.copy()

                if not d[year].get(month):
                    d[year].update({month: {}})
                    d = d.copy()

                if not d[year][month].get(day):
                    d[year][month].update({day: {}})
                    d = d.copy()

                if d[year][month][day]:
                    LabelDate = MDLabel(text = f"{month}/{day}", halign = "center", theme_text_color = "Custom", text_color = (48, 48, 48, 1), parent_background = (48, 48, 48, 1))
                    self.ids.container_chat_content.add_widget(LabelDate)

                for inday in d[year][month][day]:
                    from_id, type, message = d[year][month][day][inday]['from_id'], d[year][month][day][inday]['type'], d[year][month][day][inday]['data']

                    self.append_roundedlabel_message(from_id, type, message)

                now = now + timedelta(days=1)

            '''
            Read data not readable
            '''

            if self.new_read_conv_content.get(user_id):
                LabelDate = MDLabel(text = 'New message(s)', halign = "center", theme_text_color = "Custom", text_color = (48, 48, 48, 1), parent_background = (48, 48, 48, 1))
                self.ids.container_chat_content.add_widget(LabelDate)

                for content in self.new_read_conv_content[user_id]:
                    datatime = {
                        'year': content['time'][0],
                        'month': content['time'][1],
                        'day': content['time'][2],
                        'hour': content['time'][3],
                        'minute': content['time'][4],
                        'second': content['time'][5]
                    }
                    AddChatContent(chat_id, chat_id, 'message', content['data'], datatime)
                    self.append_roundedlabel_message("nome", content['type'], content['data'])

                del self.new_read_conv_content[user_id]

                    #append_roundedlabel_message()
        #self.ids.scroll_to(label)
