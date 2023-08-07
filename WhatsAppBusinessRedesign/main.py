import kivy
from kivymd.app import MDApp

from kivy.lang import Builder   
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivymd.uix.tab import MDTabsBase
from kivy.properties import ObjectProperty, OptionProperty, StringProperty, DictProperty, BooleanProperty
from kivymd.icon_definitions import md_icons
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from database.database import profiles
import database  
from kivymd.uix.card import MDCard


Window.size = (375, 680)    # window method to resize the application window (x, y) dimensions


Builder.load_file('kvs/pages/call_screen.kv')
Builder.load_file('kvs/pages/catalog_screen.kv')
Builder.load_file('kvs/pages/message_screen.kv')
Builder.load_file('kvs/widgets/status_layout.kv')
Builder.load_file('kvs/widgets/avatar.kv')
Builder.load_file('kvs/widgets/chat_list_item.kv')
Builder.load_file('kvs/widgets/call_list_item.kv')
Builder.load_file('kvs/widgets/bottom_navigator.kv')
Builder.load_file('kvs/widgets/text_field.kv')
Builder.load_file('kvs/widgets/chat_note.kv')


class WindowManager(ScreenManager):
    """ 
    The Window screen in a kivy screenmanager to manage switching between screens.
    (means that the WindowManager will be in this screen which is the main screen thus the name ScreenManager)
    
    """
    pass    

class MainScreen(Screen):
    """ 
    #1
    A screen for all holding the Tabs as follows catalogue, database, status and calls 
    """

class StatusIcon(MDBoxLayout):
    """
    #4
    A class for vertical Status display
    """

    text = StringProperty()
    source = StringProperty()
    time = StringProperty()
    image = ObjectProperty()

class CatalogScreen(Screen):
    """#5
    A screen for displaying catalog Tab
    This screen is added to the CatalogTab class in the main.kv file
    Remember to always start with the screen class in the screens.kv file
    For example in this class in the catalog_screen.kv file, start as shown

    <CatalogScreen>:
        ...

    """

class CallScreen(Screen):
    """
    #5
    A screen Where to display calls 

    """

class MessageScreen(Screen):
    """ #3
    A screen for displaying messages between users 
    the class is used in the create_chat method, this methos uses message builder objects to override the 
    ChatNote class (below) for displaying a chatting area in the users chat screen

    """

    text = StringProperty()
    image = ObjectProperty()
    active = BooleanProperty(default_value=False)


class ChatNote(MDBoxLayout):
    ''' 
    #3
    A chart area for users database .
    The buble is created in a different .kv file called chat_note.kv
    '''

    profile = DictProperty()
    message = StringProperty()
    time = StringProperty()
    sender = StringProperty()
    is_read = OptionProperty('waiting', options=['read', 'delivered', 'waiting'])

class ChatListItem(MDCard):
    """ 
    #2
    A chat Item holders for clicking to show database 
    Then create a database.py method to import the charts
    This is done by the chat_list_method() at the main app class
    
    """

    is_read = OptionProperty(None, options=['delivered', 'read', 'new', 'waiting'])
    friend_name = StringProperty()
    message = StringProperty()
    time_stamp = StringProperty()
    friend_profile_avatar = StringProperty()
    profile = DictProperty()


class CatalogTab(MDFloatLayout, MDTabsBase):
    """ A space for WhatsApp Business Business Profile settings """
    
    pass

class MessageTab(MDFloatLayout, MDTabsBase):
    """ A Tab screen for messages, stories and all messages and histories. """    

    pass

class StatusTab(MDFloatLayout, MDTabsBase):
    """ A Tab Screen that will be showing Statuses """

    pass

class CallsTab(MDFloatLayout, MDTabsBase):
    """ A Tab Screen for showing calls """

    pass

class MainApp(MDApp):
    """

    Always start with the Main application class 
       
    """
    

    def build(self):
        """ Then initialize the app application and return the root widget. """

        #setting theme properties
        self.title = 'WhatsApp Business Redesign'
        # self.theme_cls_style = 'Gray'  # Dark theme
        self.theme_cls.primary_palette = 'Gray' # Main color palette
        self.theme_cls.accent_palette = 'Gray' # Second color pallete with 400 hue value
        self.theme_cls_accent_hue = '400'

        #creating a list of Tabscreens


        #adding all screen in screens to the window manager
        self.wm = WindowManager(transition=FadeTransition()) # Creating an instance of Widow manager and setting the animation when switching beyween screens 

        screens = [
            MainScreen(name='main_screen')
        ]

        for screen in screens:
            self.wm.add_widget(screen)
        
        self.status_list_method()
        self.chat_list_method()
        
        return self.wm

    def switch_screen(self, screen):
        ''' A switch to change a screen using Window Manager (wm) '''
        self.wm.current = screen

    def status_list_method(self):
        ''' 
        #4
        A method for the status Tab Screen layout

        We are going to create a status for each existing user
        The StatusIcon class is used for vertical layout display
        The display is created in the status_layout.kv file which is added by the wm.screens method
        below

        '''

        for profile in database.database.profiles:
            self.status = StatusIcon()
            self.status.text = profile['name']
            self.status.source = profile['image']
            self.status.time = profile['time']
            self.wm.screens[0].ids['status_layout'].add_widget(self.status)


    def create_chat(self, profile):
        ''' 
        #3
        getting all the messages from database.py module and creating a MessageScreen.
        in this case this file is used as the database. 
        You can use Firebase/PostgreSQl at this point to use messages from a remote server
        '''

        self.chat_screen = MessageScreen()
        self.message_builder(profile, self.chat_screen)
        self.chat_screen.text = profile['name']
        self.chat_screen.image = profile['image']
        self.chat_screen.active = profile['active']
        self.wm.switch_to(self.chat_screen)

    def chat_list_method(self):
        '''         
        #2
        method for adding database in the main screen via ChatListItem class (above using MDLabel) 
        the CHATLIST is sent to the UI by chatlist id in the .kv file where it is put inside 
        a ScrollView as shown below. The screen as the main widget (MainScreen class) is used to add the ChatListItem class
        to the UI.
        '''

        # accessing data from the database.py file (from a dictionary)

        for messages in profiles:
            for message in messages['msg']:
                self.chatitem = ChatListItem()
                self.chatitem.profile = messages
                self.chatitem.friend_name = messages['name']
                self.chatitem.friend_profile_avatar = messages['image']

                lastmessage, time, is_read, sender = message.split(';') # database to be separated where there are semi-colons(all database must be 4)
                self.chatitem.message = lastmessage
                self.chatitem.time_stamp = time
                self.chatitem.is_read = is_read
                self.chatitem.sender = sender
            self.wm.screens[0].ids['chatlist'].add_widget(self.chatitem)
            
    def message_builder(self, profile, screen):
        '''
        #3
        creating a message notification for creating a chat
        the messages are in the database.py app which is a db alternative        
        '''

        for y_profile in profile['msg']:
            for messages in y_profile.split("~"):
                if messages != "":
                    message, time, is_read, sender = messages.split(";")
                    self.chat_message = ChatNote()
                    self.chat_message.message = message
                    self.chat_message.time = time
                    self.chat_message.is_read = is_read
                    self.chat_message.sender = sender
                    screen.ids['messagelist'].add_widget(self.chat_message)


if __name__ == '__main__':
    MainApp().run()












