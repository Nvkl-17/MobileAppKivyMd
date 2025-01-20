import csv
import bcrypt
from kivyauth.google_auth import initialize_google, login_google, logout_google
from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import StringProperty
from kivy.utils import get_color_from_hex
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField

Window.size = (350, 600)


class HMDApp(MDApp):
    selected_date = StringProperty("")
    def build(self):
        client_id = open("client_id.txt")
        client_secret = open("client_secret.txt")
        initialize_google(self.after_login, self.error_listener, client_id.read(), client_secret.read())
        screen = ScreenManager()
        screen.add_widget(Builder.load_file('Your.kv'))
        screen.add_widget(Builder.load_file('login.kv'))
        screen.add_widget(Builder.load_file('signup.kv'))
        screen.add_widget(Builder.load_file('home.kv'))
        screen.add_widget(Builder.load_file('result.kv'))
        return screen

    def after_login(self):
        try:
            self.root.transition.direction = "left"
            self.root.current = "home"
        except Exception as e:
            print(f"Error in after_login: {str(e)}")  # Print any exceptions for debugging

    def error_listener(self):
        print("Login Failed")

    def login(self):
        login_google()

    def logout(self):
        logout_google(self.after_logout())

    def after_logout(self):
        self.root.transition.direction = "right"
        self.root.current = "home"

    def signup(self):
        new_email = self.root.get_screen('signup').ids.em.text
        new_password = self.root.get_screen('signup').ids.pswd.text
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        with open('users.csv', 'a', newline='') as csvfile:
            fieldnames = ['Email', 'Password']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({'Email': new_email, 'Password': hashed_password})
        self.root.transition.direction = "left"
        self.root.current = "login"
        print('Sign-up successful!')

    def signin(self):
        self.root.transition.direction = "left"
        self.root.current = "home"

    def show_date_picker(self):
        date_dialog = MDDialog(
            title="Pick a Date",
            type="custom",
            content_cls=MDTextField(focus=True),
            buttons=[
                MDFlatButton(
                    text="CANCEL", text_color=get_color_from_hex("#FF5252")
                ),
                MDRaisedButton(
                    text="OK", on_release=self.set_selected_date
                ),
            ],
        )
        date_dialog.open()

    def set_selected_date(self, instance):
        hs = self.root.get_screen('result')
        date_field = hs.ids.date_field
        selected_date = instance.parent.content_cls.text
        date_field.text = selected_date
        instance.parent.parent.dismiss()

    def show_selected_date(self):
        hs = self.root.get_screen('result')
        date_field = hs.ids.date_field
        selected_date = date_field.text
        print(f"Selected Date: {selected_date}")
        
if __name__ == '__main__':
    HMDApp().run()
