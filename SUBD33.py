import tkinter as tk
from tkinter import ttk
import psycopg2
from psycopg2 import OperationalError

def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection

def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except OperationalError as e:
        print(f"The error '{e}' occurred")

class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    def init_main(self):
        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.add_img = tk.PhotoImage(file='photo333.gif')
        self.add_img1 = self.add_img.subsample(4, 4)
        btn_open_dialog = tk.Button(toolbar, text='Добавить товар', command=self.open_dialog, bg='#d7d8e0', bd=0, compound=tk.TOP, image=self.add_img1)
        btn_open_dialog.pack(side=tk.LEFT)

        self.update_img = tk.PhotoImage(file='money-clipart-gif-2.gif')
        self.upd_img2 = self.update_img.subsample(22, 26)
        btn_edit_dialog = tk.Button(toolbar, text='Редактировать', command=self.open_update_dialog, bg='#d7d8e0', bd=0, compound=tk.TOP, image=self.upd_img2)
        btn_edit_dialog.pack(side=tk.LEFT)

        btn_delete = tk.Button(toolbar, text='Удалить позицию', bg='#d7d8e0', bd=0, image=self.upd_img2,
                               compound=tk.TOP, command=self.delete_records)
        btn_delete.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(self, columns=('ID', 'Вид одежды', 'Бренд', 'Размер', 'Цена'), height=15, show='headings')
        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('Вид одежды', width=300, anchor=tk.CENTER)
        self.tree.column('Бренд', width=150, anchor=tk.CENTER)
        self.tree.column('Размер', width=85, anchor=tk.CENTER)
        self.tree.column('Цена', width=85, anchor=tk.CENTER)

        self.tree.heading('ID', text='ID')
        self.tree.heading('Вид одежды', text='Вид одежды')
        self.tree.heading('Бренд', text='Бренд')
        self.tree.heading('Размер', text='Размер')
        self.tree.heading('Цена', text='Цена')

        self.tree.pack()

    def records(self, sizes_id, brand_id, type_id, price):
        self.db.data_insert(sizes_id, brand_id, type_id, price)
        self.view_records()

    def update_record(self, sizes_id, brand_id, type_id, price):
        self.selec_pr_id = "SELECT max(id) FROM products"
        self.maxid3 = execute_read_query(self.conn, self.selec_pr_id)
        #self.db.c.execute('''UPDATE products SET price=?, TypesOfClothing_id=?, sizes_id=?, brand_id=? WHERE id=?''', (price, type_id, sizes_id, brand_id, self.selec_pr_id + 1))
        self.db.c.execute(f"INSERT INTO products (id, price, TypesOfClothing_id, sizes_id, brand_id) VALUES {self.maxid3[0][0] + 1, price, type_id, sizes_id, brand_id}")
        #self.db.c.execute(f"UPDATE volumes SET products_id=?, shops_id=? WHERE id=?", (self.maxid3[0][0] + 1, 1, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.c.execute(f"UPDATE volumes SET products_id={self.maxid3[0][0] + 1}, shops_id={1} WHERE id={self.tree.set(self.tree.selection()[0], '#1')}")

        self.db.conn.commit()
        self.view_records()
    def view_records(self):
        self.conn = create_connection("studbd_02", "adminastra", "10523411", "192.168.56.50", "5432")
        self.c = self.conn.cursor()
        self.db.c.execute('''SELECT v.id, Ty.name, br.name, si.size, p.price FROM volumes as v join products as p on v.products_id=p.id join TypesOfClothing as Ty on Ty.id=p.TypesOfClothing_id join brand as br on br.id=p.brand_id join sizes as si on si.id=p.sizes_id order by v.id''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.c.execute(f"DELETE FROM volumes WHERE id={self.tree.set(selection_item, '#1')}")
        self.db.conn.commit()
        self.view_records()

    def open_dialog(self):
        Child()

    def open_update_dialog(self):
        Update()


class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('Добавить товар')
        self.geometry('400x220+400+300')
        self.resizable(False, False)

        label_description = tk.Label(self, text='Вид одежды')
        label_description.place(x=50, y=20)

        label_price = tk.Label(self, text='Цена')
        label_price.place(x=50, y=50)

        label_brend = tk.Label(self, text='Бренд')
        label_brend.place(x=50, y=80)

        label_size = tk.Label(self, text='Размер')
        label_size.place(x=50, y=110)

        self.conn = create_connection("studbd_02", "adminastra", "10523411", "192.168.56.50", "5432")
        self.c = self.conn.cursor()
        self.select_TypesOfClothing = "SELECT * FROM TypesOfClothing"
        self.TypesOfClothing = execute_read_query(self.conn, self.select_TypesOfClothing)
        self.combobox_description = ttk.Combobox(self, values=[self.TypesOfClothing[i][0:2] for i in range(0, len(self.TypesOfClothing))])
        print(self.combobox_description)
        self.combobox_description.current(0)
        self.combobox_description.place(x=200, y=20)

        self.entry_price = ttk.Entry(self)
        self.entry_price.place(x=200, y=50)

        self.select_brand = "SELECT * FROM brand"
        self.brand = execute_read_query(self.conn, self.select_brand)
        self.combobox_brand = ttk.Combobox(self, values=[self.brand[i][0:2] for i in range(0, len(self.brand))])
        self.combobox_brand.current(0)
        self.combobox_brand.place(x=200, y=80)

        self.select_sizes = "SELECT * FROM sizes"
        self.sizes = execute_read_query(self.conn, self.select_sizes)
        self.combobox_sizes = ttk.Combobox(self, values=[self.sizes[i][0:2] for i in range(0, len(self.sizes))])
        self.combobox_sizes.current(0)
        self.combobox_sizes.place(x=200, y=110)

        btn_cansel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cansel.place(x=180, y=180)

        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=260, y=180)
        self.btn_ok.bind('<Button-1>', lambda event: self.view.records(self.combobox_sizes.get()[0], self.combobox_brand.get()[0], self.combobox_description.get()[0], self.entry_price.get()))

        self.grab_set()
        self.focus_set()

class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app

    def init_edit(self):
        self.title('редактировать позицию')
        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=260, y=180)
        btn_edit.bind('<Button-1>', lambda event: self.view.update_record(self.combobox_sizes.get()[0], self.combobox_brand.get()[0], self.combobox_description.get()[0], self.entry_price.get()))
        self.btn_ok.destroy()

class DB:
    def __init__(self):
        self.conn = create_connection("studbd_02", "adminastra", "10523411", "192.168.56.50", "5432")
        self.c = self.conn.cursor()

    def data_insert(self, sizes_id, brand_id, type_id, price):
        self.select_pr_id = "SELECT max(id) FROM products"
        self.maxid1 = execute_read_query(self.conn, self.select_pr_id)
        self.select_vlm_id = "SELECT max(id) FROM volumes"
        self.maxid2 = execute_read_query(self.conn, self.select_vlm_id)
        self.c.execute(f"INSERT INTO products (id, price, TypesOfClothing_id, sizes_id, brand_id) VALUES {self.maxid1[0][0] + 1, price, type_id, sizes_id, brand_id}")
        self.c.execute(f"INSERT INTO volumes (id, products_id, shops_id) VALUES {int(self.maxid2[0][0] + 1), int(self.maxid1[0][0] + 1), 1}")
        self.conn.commit()

if __name__=="__main__":
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title("Магазин одежды")
    root.geometry("650x450+300+200")
    root.resizable(False, False)
    root.mainloop()