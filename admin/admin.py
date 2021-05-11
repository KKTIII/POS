from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.lang import Builder
from collections import OrderedDict
from utils.datatable import DataTable
from datetime import datetime
import datetime

import mysql.connector

Builder.load_file('admin/Admin.kv')


class AdminWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mydb = mysql.connector.connect(
            host='localhost',
            user='KKT',
            passwd='CSC@15-19',
            database='supermarket'
        )
        self.mycursor = self.mydb.cursor()
        box = BoxLayout(orientation='vertical',padding=50)
        box.add_widget(Label(text="Error, Enter Values For All Fields To Continue"))
        box_2 = BoxLayout(orientation='vertical', padding=50)
        box_2.add_widget(Label(text="Please Enter Username To Proceed"))
        box_3 = BoxLayout(orientation='vertical', padding=50)
        box_3.add_widget(Label(text="User Does Not Exist. Enter Valid Username To Proceed"))
        box_4 = BoxLayout(orientation='vertical', padding=50)
        box_4.add_widget(Label(text="Please Enter Product name To Proceed"))
        box_5 = BoxLayout(orientation='vertical', padding=50)
        box_5.add_widget(Label(text="Product Does Not Exist. Enter Valid Product Name To Proceed"))
        box_6 = BoxLayout(orientation='vertical', padding=50)
        box_6.add_widget(Label(text="User Already Exists. Enter New Username to Proceed"))
        box_7 = BoxLayout(orientation='vertical', padding=50)
        box_7.add_widget(Label(text="Product Already Exists. Enter New Product name to Proceed"))
        box_8 = BoxLayout(orientation='vertical', padding=50)
        box_8.add_widget(Label(text="Kindly Enter Both Start Date and End Date to Proceed "))
        box_9 = BoxLayout(orientation='vertical', padding=50)
        box_9.add_widget(Label(text="Value Entered Is Not a Valid Date "))
        box_10 = BoxLayout(orientation='vertical', padding=50)
        box_10.add_widget(Label(text="Please Enter Product Name "))

        self.error_popup = Popup(title='Error Message',
                            content=box,
                            size_hint=(.5,.5),)
        box.add_widget(Button(text="OK", size_hint=(.4, .4), pos_hint={"center_x": .5, "center_y": .5},
                              on_press=self.error_popup.dismiss))
        self.error_popup_2 = Popup(title='Error Message',
                                 content=box_2,
                                 size_hint=(.5, .5), )
        box_2.add_widget(Button(text="OK", size_hint=(.4, .4), pos_hint={"center_x": .5, "center_y": .5},
                              on_press=self.error_popup_2.dismiss))
        self.error_popup_3 = Popup(title='Error Message',
                                   content=box_3,
                                   size_hint=(.5, .5), )
        box_3.add_widget(Button(text="OK", size_hint=(.4, .4), pos_hint={"center_x": .5, "center_y": .5},
                              on_press=self.error_popup_3.dismiss))
        self.error_popup_4 = Popup(title='Error Message',
                                   content=box_4,
                                   size_hint=(.5, .5), )
        box_4.add_widget(Button(text="OK", size_hint=(.4, .4), pos_hint={"center_x": .5, "center_y": .5},
                                on_press=self.error_popup_4.dismiss))
        self.error_popup_5 = Popup(title='Error Message',
                                   content=box_5,
                                   size_hint=(.6, .6), )
        box_5.add_widget(Button(text="OK", size_hint=(.3, .3), pos_hint={"center_x": .5, "center_y": .5},
                                on_press=self.error_popup_5.dismiss))
        self.error_popup_6 = Popup(title='Error Message',
                                   content=box_6,
                                   size_hint=(.6, .6), )
        box_6.add_widget(Button(text="OK", size_hint=(.3, .3), pos_hint={"center_x": .5, "center_y": .5},
                                on_press=self.error_popup_6.dismiss))
        self.error_popup_7 = Popup(title='Error Message',
                                   content=box_7,
                                   size_hint=(.6, .6), )
        box_7.add_widget(Button(text="OK", size_hint=(.3, .3), pos_hint={"center_x": .5, "center_y": .5},
                                on_press=self.error_popup_7.dismiss))
        self.error_popup_8 = Popup(title='Error Message',
                                   content=box_8,
                                   size_hint=(.6, .6), )
        box_8.add_widget(Button(text="OK", size_hint=(.3, .3), pos_hint={"center_x": .5, "center_y": .5},
                                on_press=self.error_popup_8.dismiss))
        self.error_popup_9 = Popup(title='Error Message',
                                 content=box_9,
                                 size_hint=(.5, .5), )
        box_9.add_widget(Button(text="OK", size_hint=(.4, .4), pos_hint={"center_x": .5, "center_y": .5},
                              on_press=self.error_popup_9.dismiss))
        self.error_popup_10 = Popup(title='Error Message',
                                   content=box_10,
                                   size_hint=(.5, .5), )
        box_10.add_widget(Button(text="OK", size_hint=(.4, .4), pos_hint={"center_x": .5, "center_y": .5},
                                on_press=self.error_popup_10.dismiss))



        #     stb = {
        #     'TH0':{0:'St0',1:'Sample1',2:'Sample2',3:'Sample4'},
        #     'TH1':{0:'Stm0',1:'Sample1',2:'Sample2',3:'Sample4'},
        #     'TH2':{0:'Stmp0',1:'Sampled1.0',2:'Sampled2.0',3:'Sampled4.0'},
        #     'TH3':{0:'Stmpl0',1:'Sample1',2:'Sample2',3:'Sample4'},
        #     'TH4':{0:'Stmple0',1:'Sample1',2:'Sample2',3:'Sample4'},
        # print(self.get_products())
        # }
        content = self.ids.scrn_contents
        users = self.get_users()
        userstable = DataTable(table=users)
        content.add_widget(userstable)

        # Display Products
        product_scrn = self.ids.scrn_product_contents
        products = self.get_products()
        prod_table = DataTable(table=products)
        product_scrn.add_widget(prod_table)

    def logout(self):
        self.parent.parent.current='scrn_si'

    def direct_to_operator(self):
        self.parent.parent.current = 'scrn_op'
        content= self.ids.transaction_display
        check_stock_content=self.ids.check_stock_display
        content.clear_widgets()
        check_stock_content.clear_widgets()
        self.ids.total.text=''
        self.ids.total.background_color=(1,1,1,1)

    def add_user_fields(self):
        target = self.ids.ops_fields
        target.clear_widgets()
        crud_first = TextInput(hint_text='First Name', multiline=False)
        crud_last = TextInput(hint_text='Last Name', multiline=False)
        crud_user = TextInput(hint_text='Username', multiline=False)
        crud_pwd = TextInput(hint_text='Password', multiline=False)
        crud_des = Spinner(text='Operator', values=['Operator', 'Administrator'])
        crud_submit = Button(text='Add', size_hint_x=None, width=100,
                             on_release=lambda x: self.add_user(crud_first.text, crud_last.text, crud_user.text,
                                                                crud_pwd.text, crud_des.text))

        target.add_widget(crud_first)
        target.add_widget(crud_last)
        target.add_widget(crud_user)
        target.add_widget(crud_pwd)
        target.add_widget(crud_des)
        target.add_widget(crud_submit)

    def add_product_fields(self):
        target = self.ids.ops_fields_p
        target.clear_widgets()
        crud_name = TextInput(hint_text='Product Name', multiline=False)
        crud_price = TextInput(hint_text='Product Price', multiline=False)
        crud_stock = TextInput(hint_text='Product Stock', multiline=False)
        crud_submit = Button(text='Add',size_hint_x=None,width=100,
                             on_release=lambda x: self.add_product(crud_name.text,crud_price.text,crud_stock.text))
        target.add_widget(crud_name)
        target.add_widget(crud_price)
        target.add_widget(crud_stock)
        target.add_widget(crud_submit)

    def add_user(self, first, last, user, pwd, des):
        content = self.ids.scrn_contents
        content.clear_widgets()
        if first=="" or last=="" or user=="" or pwd=="":
            self.error_popup.open()
        else:
            check_username_sql = 'SELECT * FROM user WHERE username=%s'
            value = [user]
            self.mycursor.execute(check_username_sql, value)
            find_user = self.mycursor.fetchone()
            if find_user != None:
                self.error_popup_6.open()
            else:
                sql = 'INSERT INTO user(first_name,last_name,username,password,designation) VALUES(%s,%s,%s,%s,%s)'
                values = [first, last, user, pwd, des]

                self.mycursor.execute(sql, values)
                self.mydb.commit()

        users = self.get_users()
        userstable = DataTable(table=users)
        content.add_widget(userstable)

    def add_product(self, name, price, stock):
        content = self.ids.scrn_product_contents
        content.clear_widgets()
        if name=="" or price=="" or stock=="":
            self.error_popup.open()
        else:
            check_product_name_sql = 'SELECT * FROM product WHERE product_name=%s'
            value = [name]
            self.mycursor.execute(check_product_name_sql, value)
            find_product = self.mycursor.fetchone()
            if find_product != None:
                self.error_popup_7.open()
            else:
                sql = 'INSERT INTO product(product_name,product_price,stock) VALUES(%s,%s,%s)'
                values = [name, price, stock]

                self.mycursor.execute(sql, values)
                self.mydb.commit()

        prodz = self.get_products()
        stocktable = DataTable(table=prodz)
        content.add_widget(stocktable)


    def update_user_fields(self):
        target = self.ids.ops_fields
        target.clear_widgets()
        crud_first = TextInput(hint_text='First Name', multiline=False)
        crud_last = TextInput(hint_text='Last Name', multiline=False)
        crud_user = TextInput(hint_text='Username', multiline=False)
        crud_pwd = TextInput(hint_text='Password', multiline=False)
        crud_des = Spinner(text='Designation', values=['Operator', 'Administrator'])
        crud_submit = Button(text='Update', size_hint_x=None, width=100,
                             on_release=lambda x: self.update_user(crud_first.text, crud_last.text, crud_user.text,
                                                                   crud_pwd.text, crud_des.text))

        target.add_widget(crud_first)
        target.add_widget(crud_last)
        target.add_widget(crud_user)
        target.add_widget(crud_pwd)
        target.add_widget(crud_des)
        target.add_widget(crud_submit)

    def update_product_fields(self):
        target = self.ids.ops_fields_p
        target.clear_widgets()

        crud_name = TextInput(hint_text='Product Name', multiline=False)
        crud_price = TextInput(hint_text='Product Price', multiline=False)
        crud_stock = TextInput(hint_text='Product Stock', multiline=False)
        crud_submit = Button(text='Update', size_hint_x=None, width=100,
                             on_release=lambda x: self.update_product(crud_name.text, crud_price.text, crud_stock.text,
                                                                      ))

        target.add_widget(crud_name)
        target.add_widget(crud_price)
        target.add_widget(crud_stock)
        target.add_widget(crud_submit)

    def update_user(self, first, last, user, pwd, des):
        content = self.ids.scrn_contents
        content.clear_widgets()
        if user=="":
            self.error_popup_2.open()
        else:
            check_username_sql = 'SELECT * FROM user WHERE username=%s'
            value=[user]
            self.mycursor.execute(check_username_sql, value)
            find_user = self.mycursor.fetchone()
            if find_user==None:
                self.error_popup_3.open()

            else:
                if first=="":
                    first=find_user[0]
                if last=="":
                    last=find_user[1]
                if pwd=="":
                    pwd=find_user[3]
                if des=="Designation":
                    des=find_user[4]
                sql = 'UPDATE user SET first_name=%s,last_name=%s,username=%s,password=%s,designation=%s WHERE username=%s'
                values = [first, last, user, pwd, des, user]

                self.mycursor.execute(sql, values)
                self.mydb.commit()

        users = self.get_users()
        userstable = DataTable(table=users)
        content.add_widget(userstable)

    def update_product(self, name, price, stock):
        content = self.ids.scrn_product_contents
        content.clear_widgets()
        if name=="":
            self.error_popup_4.open()
        else:
            check_product_name_sql = 'SELECT * FROM product WHERE product_name=%s'
            value=[name]
            self.mycursor.execute(check_product_name_sql, value)
            find_product = self.mycursor.fetchone()
            if find_product==None:
                self.error_popup_5.open()
            else:
                if price=="":
                    price=find_product[2]
                if stock=="":
                    stock=find_product[3]

                sql = 'UPDATE product SET product_name=%s,product_price=%s,stock=%s WHERE product_name=%s'
                values = [name, price,stock,name]

                self.mycursor.execute(sql, values)
                self.mydb.commit()

        prodz = self.get_products()
        stocktable = DataTable(table=prodz)
        content.add_widget(stocktable)

    def remove_user_fields(self):
        target = self.ids.ops_fields
        target.clear_widgets()
        crud_user = TextInput(hint_text='Username')
        crud_submit = Button(text='Remove', size_hint_x=None, width=100,
                             on_release=lambda x: self.remove_user(crud_user.text))

        target.add_widget(crud_user)
        target.add_widget(crud_submit)

    def remove_product_fields(self):
        target = self.ids.ops_fields_p
        target.clear_widgets()
        crud_name = TextInput(hint_text='Product Name')
        crud_submit = Button(text='Remove', size_hint_x=None, width=100,
                             on_release=lambda x: self.remove_product(crud_name.text))

        target.add_widget(crud_name)
        target.add_widget(crud_submit)

    def remove_user(self, user):
        content = self.ids.scrn_contents
        content.clear_widgets()
        if user=='':
            self.error_popup.open()
        else:
            check_username_sql = 'SELECT * FROM user WHERE username=%s'
            value = [user]
            self.mycursor.execute(check_username_sql, value)
            find_user = self.mycursor.fetchone()
            if find_user == None:
                self.error_popup_3.open()
            else:
                sql = 'DELETE FROM user WHERE username = %s'
                # self.users.remove({'user_name':user})
                values = [user]
                self.mycursor.execute(sql, values)
                self.mydb.commit()

        users = self.get_users()
        userstable = DataTable(table=users)
        content.add_widget(userstable)

    def remove_product(self, name):
        content = self.ids.scrn_product_contents
        content.clear_widgets()
        if name=="":
            self.error_popup_4.open()
        else:
            check_product_name_sql = 'SELECT * FROM product WHERE product_name=%s'
            value=[name]
            self.mycursor.execute(check_product_name_sql, value)
            find_product = self.mycursor.fetchone()
            if find_product==None:
                self.error_popup_5.open()
            else:
                sql = 'DELETE FROM product WHERE product_name = %s'
                # self.users.remove({'user_name':user})
                values = [name]
                self.mycursor.execute(sql, values)
                self.mydb.commit()

        prodz = self.get_products()
        stocktable = DataTable(table=prodz)
        content.add_widget(stocktable)

    def check_stock(self):
        mydb = mysql.connector.connect(
            host='localhost',
            user='KKT',
            passwd='CSC@15-19',
            database='supermarket'
        )
        mycursor = mydb.cursor()
        content = self.ids.check_stock_display
        content.clear_widgets()
        product_name = self.ids.check_product_input.text
        products_container = self.ids.check_stock_display
        if product_name=="":
            self.error_popup_10.open()
        else:
            sql = 'SELECT * FROM product WHERE product_name = %s'
            value = [product_name]
            mycursor.execute(sql, value)
            product_info = mycursor.fetchone()
            if product_info==None:
                self.error_popup_5.open()
            else:
                details = BoxLayout(size_hint_y=None, height=30, pos_hint={'top': 1})
                products_container.add_widget(details)
                product_id = Label(text=str(product_info[0]), size_hint_x=.2, color=(0, 0, 0, 1))
                p_name = Label(text=str(product_info[1]), size_hint_x=.2, color=(0, 0, 0, 1))
                stock = Label(text=str(product_info[3]), size_hint_x=.2, color=(0, 0, 0, 1))
                sold = Label(text=str(product_info[4]), size_hint_x=.2, color=(0, 0, 0, 1))
                details.add_widget(product_id)
                details.add_widget(p_name)
                details.add_widget(stock)
                details.add_widget(sold)

    def transaction_summary(self):
        mydb = mysql.connector.connect(
            host='localhost',
            user='KKT',
            passwd='CSC@15-19',
            database='supermarket'
        )
        mycursor = mydb.cursor()
        final_total=0
        content=self.ids.transaction_display
        total_clear=self.ids.total
        total_clear.clear_widgets()
        content.clear_widgets()
        start_date = self.ids.start_date_input.text
        end_date = self.ids.end_date_input.text
        products_container = self.ids.transaction_display
        if start_date == "" and end_date == "":
            self.error_popup_8.open()
            self.ids.transaction_display.clear_widgets()
        else:
            if start_date!='' and end_date=="":
                sql = 'SELECT transaction_id,date,total,operator,products_bought FROM transaction WHERE DATE(date) =  %s'
                values = [start_date]
                try:
                    datetime.datetime.strptime(start_date, '%Y-%m-%d')
                except ValueError:
                    self.error_popup_9.open()
                    self.ids.transaction_display.clear_widgets()
            else:
                sql = 'SELECT transaction_id,date,total,operator,products_bought FROM transaction WHERE DATE(date) BETWEEN %s AND %s'
                values = [start_date,end_date]
                try:
                    datetime.datetime.strptime(start_date, '%Y-%m-%d')
                    datetime.datetime.strptime(end_date, '%Y-%m-%d')
                except ValueError:
                    self.error_popup_9.open()
                    self.ids.transaction_display.clear_widgets()
            mycursor.execute(sql, values)
            transactions = mycursor.fetchall()
            if transactions==None:
                pass
            else:
                for transaction in transactions:
                    details = BoxLayout(size_hint_y=None, height=30, pos_hint={'top': 1})
                    products_container.add_widget(details)
                    date = Label(text=str(f'{transaction[1]:%Y-%m-%d}'), size_hint_x=.2, color=(0, 0, 0, 1))
                    transaction_id = Label(text=str(transaction[0]), size_hint_x=.2, color=(0, 0, 0, 1))
                    total = Label(text=str(transaction[2]), size_hint_x=.2, color=(0, 0, 0, 1))
                    operator = Label(text=str(transaction[3]), size_hint_x=.2, color=(0, 0, 0, 1))
                    purchased=Label(text=str(transaction[4]), size_hint_x=.8, color=(0, 0, 0, 1))
                    details.add_widget(transaction_id)
                    details.add_widget(date)
                    details.add_widget(total)
                    details.add_widget(operator)
                    details.add_widget(purchased)
                    final_total = final_total + transaction[2]
            final_show = 'Total: ' + str(final_total)
            show=self.ids.total
            show.text=final_show
            show.background_color=(140/255,158/255,237/255,1)



    def get_users(self):
        mydb = mysql.connector.connect(
            host='localhost',
            user='KKT',
            passwd='CSC@15-19',
            database='supermarket'
        )
        mycursor = mydb.cursor()
        _users = OrderedDict()
        _users['First Name'] = {}
        _users['Last Name'] = {}
        _users['Username'] = {}
        _users['Designation'] = {}
        _users['Date Added'] = {}
        first_names = []
        last_names = []
        usernames = []
        designations = []
        date = []

        sql = 'SELECT * FROM user'
        mycursor.execute(sql)
        users = mycursor.fetchall()
        for user in users:
            first_names.append(user[0])
            last_names.append(user[1])
            usernames.append(user[2])
            designations.append(user[4])
            date.append(user[5])
        # print(designations)
        users_length = len(first_names)
        idx = 0
        while idx < users_length:
            _users['First Name'][idx] = first_names[idx]
            _users['Last Name'][idx] = last_names[idx]
            _users['Username'][idx] = usernames[idx]
            _users['Designation'][idx] = designations[idx]
            _users['Date Added'][idx] = f'{date[idx]:%Y-%m-%d}'

            idx += 1

        return _users

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

    def change_screen(self, instance):
        if instance.text == 'Manage Products':
            self.ids.scrn_mngr.current = 'scrn_product_content'
        elif instance.text == 'Manage Users':
            self.ids.scrn_mngr.current = 'scrn_content'
        elif instance.text == 'Check Stock':
            self.ids.scrn_mngr.current = 'scrn_check'
        else:
            self.ids.scrn_mngr.current = 'scrn_analysis'


class AdminApp(App):
    def build(self):
        return AdminWindow()


if __name__ == '__main__':
    AdminApp().run()