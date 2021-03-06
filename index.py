from sqlite3 import dbapi2
from tkinter import ttk
from tkinter import *
import sqlite3

class Product: 

    db_Name = 'database.db'

    def __init__(self,window):
        self.wind = window
        self.wind.title('Products Application')
        self.wind.resizable(0,0)

        #Creating Frames Containers
        frame = LabelFrame(self.wind, text = 'Register a new product')
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)
      
        
        # Name inputs
        Label(frame, text = 'Name: ').grid(row = 1, column = 0)
        self.name = Entry(frame) 
        self.name.focus()
        self.name.grid(row = 1, column = 1)

        # Price Input
        Label(frame, text = 'Price: ').grid(row = 2, column = 0)
        self.price = Entry(frame)
        self.price.grid(row = 2, column = 1)

        # Button add product
        ttk.Button(frame, text = 'Save Product', command = self.add_product, cursor = 'hand2').grid(row = 3, columnspan = 2, sticky = W + E)
        

        # Output Messages
        self.message = Label(text ='',fg = 'red')
        self.message.grid(row = 4, column = 0, columnspan = 2, sticky = W+E) 

        # Table
        self.tree = ttk.Treeview(height = 10, columns = 2)
        self.tree.grid(row = 5, column = 0, columnspan = 2)
        self.tree.heading('#0', text = 'Name', anchor = CENTER)
        self.tree.heading('#1', text = 'Price', anchor = CENTER)

        # Buttons
        ttk.Button(text = 'Delete Product', command = self.delete_product, cursor = 'hand2').grid(row = 6, column = 0, sticky = W + E)
        ttk.Button(text = 'Edit Product', command = self.edit_product, cursor = 'hand2').grid(row = 6, column = 1, sticky = W + E)


        # filling the rows
        self.get_product()

    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_Name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
            return result

    def get_product(self):
        # cleaning table
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        # quering
        query = 'SELECT * FROM product ORDER BY name DESC'
        db_rows = self.run_query(query)
        for row in db_rows:
            self.tree.insert('',0, text = row[1], values = row[2])

    def add_product(self):
        if self.validation():
            query = 'INSERT INTO product VALUES(NULL, ?, ?)'
            parameters = (self.name.get(), self.price.get())
            self.run_query(query, parameters) 
            self.message['text'] = 'Product {} added successfully'.format(self.name.get())
            self.name.delete(0, END) 
            self.price.delete(0, END) 
            
        else:
            self.message['text'] = 'Name and Price are required'
        self.get_product()

    def validation(self):
        return len(self.name.get()) != 0 and len(self.price.get()) != 0

    def delete_product(self):
        self.message['text'] = ''
        try: 
            self.tree.item(self.tree.selection())['text'][0] 
        except IndexError as e:
            self.message['text'] = 'Please select a record'
            return
        self.message['text'] = ''
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM product WHERE name = ?'
        self.run_query(query,(name, ))
        self.message['text'] = 'Record {} has been deleted Successfully'.format(name)
        self.get_product()

    def edit_product(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Please select a record'
            return

        name = self.tree.item(self.tree.selection())['text']
        old_price = self.tree.item(self.tree.selection())['values'][0]

        # Create new window
        self.edit_wind = Toplevel()
        self.edit_wind.title('Edit Product')
        self.edit_wind.resizable(0,0)
        
        # Old name
        Label(self.edit_wind, text = 'Old name: ').grid(row = 0, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = name), state = 'readonly').grid(row = 0, column = 2)

        # New Name
        Label(self.edit_wind, text = 'New name: ').grid(row = 1, column = 1)
        new_name = Entry(self.edit_wind)
        new_name.grid(row = 1, column = 2)

        # Old price
        Label(self.edit_wind, text = 'Old price: ').grid(row = 2, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_price), state = 'readonly').grid(row = 2, column = 2)

        # New price
        Label(self.edit_wind, text = 'New price: ').grid(row = 3, column = 1)
        new_price = Entry(self.edit_wind)
        new_price.grid(row = 3, column = 2)

        # Save Button
        Button(self.edit_wind, text = 'Update', command = lambda : self.edit_records (new_name.get(), name, new_price.get(), old_price), cursor = 'hand2').grid(row = 4, column = 0, sticky = W + E)
        # Cancel Button
        Button(self.edit_wind, text = 'Cancel', command = lambda : self.edit_wind.destroy(), cursor = 'hand2').grid(row = 4, column = 1, sticky = W + E)


    def edit_records(self,new_name, name, new_price, old_price):
        if new_name == '':
            new_name = name

        if new_price == '':
            new_price = old_price

        query = 'UPDATE product SET name = ?, price = ? WHERE name = ? AND price = ?'
        parameters = (new_name, new_price, name, old_price)
        self.run_query(query, parameters) 
        self.edit_wind.destroy()
        if new_price == old_price and new_name == name:
            self.message['text'] = 'Record {} has not been updated'.format(name)
        else: 
            self.message['text'] = 'Record {} has been updated successfully'.format(name)
        self.get_product()





if __name__ == "__main__": 
    window = Tk()
    application = Product(window)
    window.mainloop() 