# MIT License
#
# Copyright (c) 2021 pyobtimus
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

''' CLASSIC MODULES '''
import json
import platform
from os import listdir, path, unlink, makedirs, remove
from threading import Thread
from plyer import battery

''' KIVY CONFIG MODULES '''
from kivy.lang import Builder
from kivy.config import Config

''' KIVY / KIVYMD MODULES '''
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen

''' All kivy screens '''

Builder.load_file('baobapp/screens/home/screen.kv')
Builder.load_file('baobapp/screens/chat/screen.kv')

from baobapp.screens.home.screen import HomeScreen
from baobapp.screens.chat.screen import ChatScreen

'''A window manager to manage switching between screens.'''
class GlobalScreenManager(ScreenManager):

    def __init__(self, **kwargs):

        super(GlobalScreenManager, self).__init__(**kwargs)

        ''' Setup DPI Config for increase the readability of the kivy application '''
        if platform.system() == "Windows":
            from ctypes import windll
            ''' Setting for remove blur from windows '''
            windll.shcore.SetProcessDpiAwareness(1)

        self.chatscreen = ChatScreen(socket_list, name='chat')
        self.homescreen = HomeScreen(name='home')

        screens = [self.homescreen, self.chatscreen]

        for screen in screens:
            self.add_widget(screen)

        self.socket_listening = Clock.schedule_interval(self.chatscreen.read_recv_data, 3)

        self.home_builder()

        """
        Plyer test
        """
        #print(battery.status)
        #audio.file_path = "baobapp/db/sound/start_app.wav"
        #audio.start()

    def on_start(self):
        pass

    def home_builder(self):
        self.homescreen.conv_inactive_list_builder()

    def change_screen(self, screen_name: str, args = []):

        screen_leaved = self.current

        if screen_leaved == "chat":
            self.chatscreen.ids.container_chat_content.clear_widgets()
            self.chatscreen.ids.input_chat_text.text = ""

        if screen_name == 'home':
            self.home_builder()
        elif screen_name == "chat":
            self.chatscreen.change_screen_to_start_chat(args)

        self.current = screen_name

    def exit(self):
        Clock.unschedule(self.socket_listening)
        self.stop()

''' Build KivyMD app '''
class MainApp(MDApp):

    def build(self):

        #self.theme_cls.theme_style = "Dark"
        self.icon = ('db/img/logo.jpg')

        return GlobalScreenManager()

''' Starting application '''
def start_app(_socket_list):
    global socket_list
    socket_list = _socket_list
    try:
        app = MainApp()
        app.run()
    except Exception as e:
        print('LOG error :', e)
        raise