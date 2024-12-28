from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.list import (
    MDListItem,
    MDListItemHeadlineText,
    MDListItemSupportingText,
    MDListItemTertiaryText
)
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogButtonContainer,
    MDDialogContentContainer,
    MDDialogHeadlineText,
    MDDialogIcon,
)
from kivymd.uix.textfield import (
    MDTextField,
    MDTextFieldHintText
)
from kivymd.uix.appbar import (
    MDTopAppBar,
    MDTopAppBarLeadingButtonContainer,
    MDActionBottomAppBarButton,
    MDTopAppBarTitle
)

from kivy.uix.screenmanager import ScreenManager

import requests

class MyCard(MDCard):
    '''Implements a material card.'''


class Fuel(MDApp):
    def build(self):
        self.screen_manager = ScreenManager()
        self.main_screen = MDScreen(
            name = "main",
            theme_bg_color="Custom",
            md_bg_color=self.theme_cls.backgroundColor,
        )
        self.card_info = MDScreen(
            name = "info",
            theme_bg_color="Custom",
            md_bg_color=self.theme_cls.backgroundColor,
        )
        self.screen_manager.add_widget(self.main_screen)
        self.screen_manager.add_widget(self.card_info)
        self.screen_manager.current = 'main'
        self.main_layout = MDBoxLayout(
            id="box",
            adaptive_size=True,
            spacing="12dp",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            orientation = "vertical",
        )
        self.main_screen.add_widget(self.main_layout)
        return self.screen_manager

    def on_start(self):
        cards_balance = self.get_cards_balance()

        print(cards_balance)

        tarjeta_8020 = MyCard(
                MDRelativeLayout(
                    MDLabel(
                        text="9760 XXXX XXXX 8020",
                        pos=("12dp", "12dp"),
                    ),
                    MDLabel(
                        text="Saldo: " + str(cards_balance["0"]) + " USD",
                        adaptive_size=True,
                        pos=("12dp", "12dp"),
                    )
                ),
                style="outlined",
                padding="4dp",
                size_hint=(None, None),
                size=("240dp", "100dp"),
                ripple_behavior=True,
                on_release = lambda x: self.get_details("8020")
            )
        tarjeta_4964 = MyCard(
                MDRelativeLayout(
                    MDLabel(
                        text="9760 XXXX XXXX 4964",
                        pos=("12dp", "12dp"),
                    ),
                    MDLabel(
                        text="Saldo: " + str(cards_balance["2"]) + " USD",
                        adaptive_size=True,
                        pos=("12dp", "12dp"),
                    )
                ),
                style="outlined",
                padding="4dp",
                size_hint=(None, None),
                size=("240dp", "100dp"),
                ripple_behavior=True,
                on_release = lambda x: self.get_details("4964")
            )
        tarjeta_3285 = MyCard(
                MDRelativeLayout(
                    MDLabel(
                        text="9760 XXXX XXXX 3285",
                        pos=("12dp", "12dp"),
                    ),
                    MDLabel(
                        text="Saldo: " + str(cards_balance["1"]) + " USD",
                        adaptive_size=True,
                        pos=("12dp", "12dp"),
                    )
                ),
                style="outlined",
                padding="4dp",
                size_hint=(None, None),
                size=("240dp", "100dp"),
                ripple_behavior=True,
                on_release = lambda x: self.get_details("3285")
            )
        self.main_layout.add_widget(tarjeta_8020)
        self.main_layout.add_widget(tarjeta_4964)
        self.main_layout.add_widget(tarjeta_3285)

    def display_info(self, card, balance, last_op_type, last_op_amount, last_op_date):
        self.screen_manager.current = 'info'

        self.card_layout = MDRelativeLayout()
        self.card_info.add_widget(self.card_layout)
        
        self.card_info_appbar = MDTopAppBar(
            MDTopAppBarLeadingButtonContainer(
                MDActionBottomAppBarButton(
                    icon = "arrow-left",
                    on_release = lambda x: self.back_action()
                ),
            ),
            MDTopAppBarTitle(
                text = "Detalles de la Tarjeta",
                pos_hint = {"center_x": 0.5}
            ),
            pos_hint={"center_y": 0.95}
        )
        self.balance_label = MDLabel(
            text="Saldo disponible",
            halign="center",
            font_style = "Headline",
            role = "small",
            pos_hint={"center_y": 0.86},
        )
        self.balance_quantity = MDLabel(
            text= "$" + balance + " USD",
            halign="center",
            font_style = "Display",
            role = "medium",
            pos_hint={"center_y": 0.77},
        )
        self.depositar_btn = MDButton(
            MDButtonText(
                text = "Depositar"
            ),
            style = "outlined",
            pos_hint={"center_x":0.42, "center_y": 0.7},
            on_release = lambda x:self.show_operation_dialog(card, "Depositar")
        )
        self.despacho_btn = MDButton(
            MDButtonText(
                text = "Despacho"
            ),
            style = "outlined",
            pos_hint={"center_x":0.58, "center_y": 0.7},
            on_release = lambda x:self.show_operation_dialog(card, "Despacho")
        )
        self.last_op_list = MDListItem(
            MDListItemHeadlineText(
                text = last_op_type
            ),
            MDListItemSupportingText(
                text = "Monto: " + last_op_amount + " USD"
            ),
            MDListItemTertiaryText(
                text = "Fecha: " + last_op_date
            ),
            pos_hint={"center_x":0.5, "center_y": 0.55},
        )

        self.card_layout.add_widget(self.card_info_appbar)
        self.card_layout.add_widget(self.balance_label)
        self.card_layout.add_widget(self.balance_quantity)
        self.card_layout.add_widget(self.depositar_btn)
        self.card_layout.add_widget(self.despacho_btn)
        self.card_layout.add_widget(self.last_op_list)

    def get_cards_balance(self):
        url = 'https://alejandroperezhdez.pythonanywhere.com/v1/fuelbalance'
        data = requests.get(url=url)

        API_DATA = data.json()
        return API_DATA

    def get_details(self, card_number):
        url = 'https://alejandroperezhdez.pythonanywhere.com/v1/fuelquery'
        params = {'card_number': card_number}
        data = requests.get(url=url, params=params)
        API_DATA = data.json()

        card = str(API_DATA['card_number']).replace("['", "").replace("']", "")
        balance = str(API_DATA['balance']).replace("['", "").replace("']", "")
        last_op = str(API_DATA['last_op']).replace("['", "").replace("']", "")

        last_op_splitted = last_op.split(",")
        last_op_type = last_op_splitted[0]
        last_op_amount = last_op_splitted[2]
        last_op_date = last_op_splitted[1]

        self.display_info(card, balance, last_op_type, last_op_amount, last_op_date)

    def depositar(self, card, amount):
        url = 'https://alejandroperezhdez.pythonanywhere.com/v1/fueldeposito'
        params = {'card_number': card, 'amount': amount}
        data = requests.get(url=url, params=params)

        self.card_layout.clear_widgets()
        self.get_details(card)

    def despacho(self, card, amount):
        url = 'https://alejandroperezhdez.pythonanywhere.com/v1/fueldespacho'
        params = {'card_number': card, 'amount': amount}
        data = requests.get(url=url, params=params)

        self.card_layout.clear_widgets()
        self.get_details(card)

    def show_operation_dialog(self, card, op_type):
        def close(obj):
            self.op_dialog.dismiss()

        def make_op(amount):
            if op_type == "Depositar":
                self.depositar(card, amount)
            elif op_type == "Despacho":
                self.despacho(card, amount)
            
            self.op_dialog.dismiss()
        
        self.dialog_icon = MDDialogIcon(icon = "ticket")
        self.dialog_headline_text = MDDialogHeadlineText()

        if op_type == "Depositar":
            self.dialog_headline_text.text = "Depositar"
        elif op_type == "Despacho":
            self.dialog_headline_text.text = "Despacho"
        
        self.content_container = MDDialogContentContainer(orientation = "vertical")

        self.amount_input = MDTextField(
                        MDTextFieldHintText(
                            text = "Monto"
                        ),
                        mode = "outlined",
                        required = True,
                        input_type = "number"
                    )
        
        self.button_container = MDDialogButtonContainer(
                    MDButton(
                        MDButtonText(text = "Cancelar"),
                        style="text",
                        on_release=close
                    ),
                    MDButton(
                        MDButtonText(text = "Aceptar"),
                        style="text",
                        on_release=lambda x:make_op(self.amount_input.text)
                    ),
                    spacing="8dp",
                )
        
        self.content_container.add_widget(self.amount_input)

        self.op_dialog = MDDialog()
        self.op_dialog.add_widget(self.dialog_icon)
        self.op_dialog.add_widget(self.dialog_headline_text)
        self.op_dialog.add_widget(self.content_container)
        self.op_dialog.add_widget(self.button_container)
        self.op_dialog.open()

    def back_action(self):
        self.main_layout.clear_widgets()
        self.screen_manager.current = 'main'
        self.on_start()

Fuel().run()