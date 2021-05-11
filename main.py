from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from admin.admin import AdminWindow
from signin.SignIn import SignInWindow
from vendor.Vendor import VendorWindow



class MainWindow(BoxLayout):

    admin_widget = AdminWindow()
    signin_widget = SignInWindow()
    vendor_widget = VendorWindow()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.ids.scrn_si.add_widget(self.signin_widget)
        self.ids.scrn_admin.add_widget(self.admin_widget)
        self.ids.scrn_op.add_widget(self.vendor_widget)


class MainApp(App):
    def build(self):

        return MainWindow()


if __name__=='__main__':
    MainApp().run()