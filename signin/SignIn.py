from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
import mysql.connector
from kivy.lang import Builder
from collections import OrderedDict
from utils.datatable import DataTable



Builder.load_file('signin/SignIn.kv')


class SignInWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mydb = mysql.connector.connect(
            host='localhost',
            user='KKT',
            passwd='CSC@15-19',
            database='supermarket'
        )
        self.mycursor = self.mydb.cursor()

    def get_products(self):
        mydb = mysql.connector.connect(
            host='localhost',
            user='KKT',
            passwd='CSC@15-19',
            database='supermarket'
        )
        mycursor = mydb.cursor()
        _stocks = OrderedDict()
        _stocks['Product Id'] = {}
        _stocks['Product Name'] = {}
        _stocks['Product Price'] = {}
        _stocks['Stock'] = {}
        _stocks['Sold'] = {}

        product_id = []
        product_name = []
        product_price = []
        stock = []
        sold = []
        sql = 'SELECT * FROM product'
        mycursor.execute(sql)
        products = mycursor.fetchall()
        for product in products:
            product_id.append(product[0])
            name = product[1]
            if len(name) > 30:
                name = name[:30] + '...'
            product_name.append(name)
            product_price.append(product[2])
            stock.append(product[3])
            sold.append(product[4])

        # print(designations)
        products_length = len(product_id)
        idx = 0
        while idx < products_length:
            _stocks['Product Id'][idx] = product_id[idx]
            _stocks['Product Name'][idx] = product_name[idx]
            _stocks['Product Price'][idx] = product_price[idx]
            _stocks['Stock'][idx] = stock[idx]
            _stocks['Sold'][idx] = sold[idx]

            idx += 1

        return _stocks

    def validate_user(self):
        u_name = self.ids.username_field.text
        pwd = self.ids.pwd_field.text
        info = self.ids.info
        self.ids.username_field.text=''
        self.ids.pwd_field.text=''
        if u_name == '' or pwd == '':
            info.text = '[color=#FF0000]Username and/or Password Required[/color]'
        else:
            check_username_sql = 'SELECT * FROM user WHERE username=%s'
            value = [u_name]
            self.mycursor.execute(check_username_sql, value)
            find_user = self.mycursor.fetchone()
            if find_user==None:
                info.text = '[color=#FF0000]User Does Not Exist[/color]'
            else:
                if pwd == find_user[3]:
                    des = find_user[4]
                    info.text = ''
                    self.parent.parent.parent.ids.scrn_op.children[0].ids.loggedin_user.text=find_user[2]
                    if des=='Administrator':
                        self.parent.parent.current = 'scrn_admin'
                        self.parent.parent.parent.ids.scrn_admin.children[0].ids.loggedin_user.text = find_user[2]
                        content = self.parent.parent.parent.ids.scrn_admin.children[0].ids.scrn_product_contents
                        content.clear_widgets()
                        prodz = self.get_products()
                        stocktable = DataTable(table=prodz)
                        content.add_widget(stocktable)

                        self.parent.parent.parent.ids.scrn_op.children[0].ids.sub_header.text='Go Back'
                    else:
                        self.parent.parent.current = 'scrn_op'
                        self.parent.parent.parent.ids.scrn_op.children[0].ids.sub_header.text = ''
                else:
                    info.text = '[color=#FF0000]Invalid Username and/or Password[/color]'


class SignInApp(App):
    def build(self):
        return SignInWindow()


if __name__ == "__main__":
    sa = SignInApp()
    sa.run()
