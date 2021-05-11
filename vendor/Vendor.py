from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.uix.popup import Popup
from utils.datatable import DataTable
from collections import OrderedDict

from kivy.uix.button import Button
from datetime import datetime
import re
import mysql.connector

Builder.load_file('vendor/Vendor.kv')


class VendorWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mydb = mysql.connector.connect(
            host='localhost',
            user='KKT',
            passwd='CSC@15-19',
            database='supermarket'
        )
        self.mycursor = self.mydb.cursor()
        self.ids.receipt_preview.text = "The Supermarket\Accra, Ghana, Space\n\nTel: XXX-XXX-XXX\nReceipt No: \nDate:" + str(datetime.date(datetime.now())) +"\n\n"

        box = BoxLayout(orientation='vertical', padding=50)
        box.add_widget(Label(text="Product Entered Does Not Exist"))
        self.error_popup = Popup(title='Error Message',
                                 content=box,
                                 size_hint=(.5, .5), )
        box.add_widget(Button(text="OK", size_hint=(.4, .4), pos_hint={"center_x": .5, "center_y": .5},
                              on_press=self.error_popup.dismiss))

        box2 = BoxLayout(orientation='vertical', padding=50)
        box2.add_widget(Label(text="Invalid Quantity Entered"))
        self.error_popup_2 = Popup(title='Error Message',
                                 content=box2,
                                 size_hint=(.5, .5), )
        box2.add_widget(Button(text="OK", size_hint=(.4, .4), pos_hint={"center_x": .5, "center_y": .5},
                              on_press=self.error_popup_2.dismiss))

        self.cart = []
        self.qty = []
        self.final_cart = {}
        self.total = 0.00

    def go_back(self):
        content= self.parent.parent.parent.ids.scrn_admin.children[0].ids.scrn_product_contents
        content.clear_widgets()
        prodz = self.get_products()
        stocktable = DataTable(table=prodz)
        content.add_widget(stocktable)
        current_user=self.ids.loggedin_user.text
        sql = "SELECT designation FROM user WHERE username=%s"
        value = [current_user]
        self.mycursor.execute(sql, value)
        find_user = self.mycursor.fetchone()
        user=find_user[0]
        if user=="Administrator":
            self.parent.parent.current = "scrn_admin"
        else:
            self.parent.parent.current = "scrn_op"

    def logout(self):
        self.parent.parent.parent.ids.scrn_op.children[0].ids.sub_header.text = 'Go Back'
        self.parent.parent.current="scrn_si"

    def check_product(self):
        display=self.ids.product_name_input.text
        sql="SELECT product_name FROM product WHERE product_name LIKE %s"
        value=['%'+ str(display) +'%']
        self.mycursor.execute(sql, value)
        find_product_name = self.mycursor.fetchall()
        products_list=[]
        for product in find_product_name:
            products_list.append(product)
        self.ids.spinner_id.values =[str(t)[2:len(t)-4] for t in products_list]
        self.ids.spinner_id.text="Select Product"

    def product_choice(self,choice):
        self.ids.product_name_input.text=choice


    def cancel_transaction(self):
        self.ids.products.clear_widgets()
        self.cart = []
        self.qty = []
        self.final_cart={}
        self.total = 0.00
        self.ids.receipt_preview.text="The Supermarket\Accra, Ghana, Space\n\nTel: XXX-XXX-XXX\nReceipt No: \nDate:" + str(datetime.date(datetime.now())) +"\n\n"


    def update_transaction(self):
        find_username=self.ids.loggedin_user.text
        total_products_bought = ""
        if not self.final_cart:
            self.parent.parent.current = 'scrn_op'
        else:
            for product_name,quantity in self.final_cart.items():
                sql="SELECT stock,sold FROM product WHERE product_name=%s"
                value=[product_name]
                self.mycursor.execute(sql, value)
                result = self.mycursor.fetchone()
                old_stock=result[0]
                old_sold = result[1]
                new_stock = old_stock - quantity
                new_sold = old_sold + quantity
                update_sql= "UPDATE product SET stock=%s, sold=%s WHERE product_name=%s"
                values= [new_stock,new_sold,product_name]
                self.mycursor.execute(update_sql, values)
                self.mydb.commit()
                total_products_bought+=str(product_name)+"["+str(quantity) +"],"
            update_transaction_sql="INSERT INTO  transaction (total,operator,products_bought) VALUES (%s,%s,%s)"
            transaction_values=[self.total,find_username,total_products_bought]
            self.mycursor.execute(update_transaction_sql, transaction_values)
            self.mydb.commit()
            self.ids.products.clear_widgets()
            self.cart = []
            self.qty = []
            self.final_cart = {}
            self.total = 0.00
            self.ids.receipt_preview.text = "The Supermarket\Accra, Ghana, Space\n\nTel: XXX-XXX-XXX\nReceipt No: \nDate:" + str(datetime.date(datetime.now())) +"\n\n"




    def update_purchases(self):
        product_name = self.ids.product_name_input.text
        products_container = self.ids.products
        sql = 'SELECT * FROM product WHERE product_name=%s'
        value=[product_name]
        self.mycursor.execute(sql,value)
        products = self.mycursor.fetchone()
        if self.ids.qty_inp.text == "":
            buying_quantity = "1"
        else:
            buying_quantity=self.ids.qty_inp.text

        if products==None:
            self.error_popup.open()
        else:
            if int(self.ids.qty_inp.text) <= 0:
                self.error_popup_2.open()
            try:
                int(self.ids.qty_inp.text)
                details = BoxLayout(size_hint_y=None, height=30, pos_hint={'top': 1})
                products_container.add_widget(details)
                mini_total = float(buying_quantity) * products[2]
                code = Label(text=str(products[0]), size_hint_x=.2, color=(0, 0, 0, 1))
                name = Label(text=str(products[1]), size_hint_x=.3, color=(0, 0, 0, 1))
                qty = Label(text=buying_quantity, size_hint_x=.1, color=(0, 0, 0, 1))
                disc = Label(text='0.00', size_hint_x=.1, color=(0, 0, 0, 1))
                price = Label(text=str(products[2]), size_hint_x=.1, color=(0, 0, 0, 1))
                total = Label(text=str(mini_total), size_hint_x=.2, color=(0, 0, 0, 1))
                details.add_widget(code)
                details.add_widget(name)
                details.add_widget(qty)
                details.add_widget(disc)
                details.add_widget(price)
                details.add_widget(total)

                # Update Preview

                product_price = mini_total
                self.total += product_price
                purchase_total = '`\n___________________________________\n\nTotal\t\t\t\t\t\t\t\t' + str(self.total)
                self.ids.current_product.text = product_name
                self.ids.current_price.text = str(product_price)
                preview = self.ids.receipt_preview
                prev_text = preview.text
                _prev = prev_text.find('`')
                if _prev > 0:
                    prev_text = prev_text[:_prev]

                ptarget = -1
                for i, c in enumerate(self.cart):
                    if c == product_name:
                        ptarget = i

                if ptarget >= 0:
                    product_qty = self.qty[ptarget] + int(buying_quantity)
                    self.qty[ptarget] = product_qty
                    self.final_cart[product_name] = product_qty
                    expr = '%s\t\tx\d\t' % (product_name)
                    rexpr = product_name + '\t\tx' + str(product_qty) + '\t'
                    new_text = re.sub(expr, rexpr, prev_text)
                    preview.text = new_text + purchase_total
                else:
                    self.cart.append(product_name)
                    self.qty.append(int(buying_quantity))
                    self.final_cart[product_name]=int(buying_quantity)
                    new_preview = '\n'.join(
                        [prev_text, product_name + '\t\tx' + buying_quantity + '\t\t' + str(product_price),
                         purchase_total])
                    preview.text = new_preview
            except ValueError:
                self.error_popup_2.open()

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


class VendorApp(App):
    def build(self):
        return VendorWindow()


if __name__== "__main__":
    oa = VendorApp()
    oa.run()
