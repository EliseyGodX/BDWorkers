import tkinter as tk
from tkinter import ttk
import sqlite3

# класс главного окна
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    # инициализация виджетов главного окна
    def init_main(self):
        toolbar = tk.Frame(bg='#6868b3', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        
        # кнопка добавления
        self.img_add = tk.PhotoImage(file='./img/add.png')
        btn_add = tk.Button(toolbar, text='Add', bg='#d7d7d7',
                            bd=0, image=self.img_add,
                            command=self.open_child)
        btn_add.pack(side=tk.LEFT)

        # кнопка изменения
        self.img_upd = tk.PhotoImage(file='./img/update.png')
        btn_upd = tk.Button(toolbar, bg='#d7d7d7',
                            bd=0, image=self.img_upd,
                            command=self.open_update_child)
        btn_upd.pack(side=tk.LEFT)
        
        # кнопка удаления
        self.img_del = tk.PhotoImage(file='./img/delete.png')
        btn_del = tk.Button(toolbar, bg='#d7d7d7',
                            bd=0, image=self.img_del,
                            command=self.delete_records)
        btn_del.pack(side=tk.LEFT)

        # кнопка поиска
        self.img_search = tk.PhotoImage(file='./img/search.png')
        btn_search = tk.Button(toolbar, bg='#d7d7d7',
                            bd=0, image=self.img_search,
                            command=self.open_search)
        btn_search.pack(side=tk.LEFT)

        # кнопка обновления
        self.img_refresh = tk.PhotoImage(file='./img/refresh.png')
        btn_refresh = tk.Button(toolbar, bg='#d7d7d7',
                            bd=0, image=self.img_refresh,
                            command=self.view_records)
        btn_refresh.pack(side=tk.RIGHT)

        # создание таблицы
        self.tree = ttk.Treeview(self, 
                                 columns=('id', 'name', 'phone', 'email', 'salary'),
                                 height=17,
                                 show='headings')
        
        self.tree.column('id', width=45, anchor=tk.CENTER)
        self.tree.column('name', width=300, anchor=tk.CENTER)
        self.tree.column('phone', width=150, anchor=tk.CENTER)
        self.tree.column('email', width=150, anchor=tk.CENTER)
        self.tree.column('salary', width=150, anchor=tk.CENTER)

        self.tree.heading('id', text='ID')
        self.tree.heading('name', text='Name')
        self.tree.heading('phone', text='Telephone')
        self.tree.heading('email', text='E-mail')
        self.tree.heading('salary', text='Salary')
        self.tree.pack(side=tk.LEFT)

        # # добавление скроллбара
        # scroll = tk.Scrollbar(self, command=self.tree.yview)
        # scroll.pack(side=tk.RIGHT, fill=tk.Y)
        # self.tree.configure(yscrollcommand=scroll.set)

        scroll = tk.Scrollbar(root, command=self.tree.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

    # метод добавления данных 
    def records(self, name, phone, email, salary):
        self.db.insert_data(name, phone, email, salary)
        self.view_records()

    # отображение данных в treeview
    def view_records(self):
        self.db.cursor.execute('SELECT * FROM personal')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=i) for i in self.db.cursor.fetchall()]

    # метод поиска данных
    def search_records(self, name):
        self.db.cursor.execute('SELECT * FROM personal WHERE name LIKE ?', 
                            ('%' + name + '%', ))
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=i) for i in self.db.cursor.fetchall()]

    # метод изменения данных
    def update_record(self, name, phone, email, salary):
        id = self.tree.set(self.tree.selection()[0], '#1')
        self.db.cursor.execute('''
            UPDATE personal 
            SET name = ?, phone = ?, email = ?, salary = ?
            WHERE id = ?
        ''', (name, phone, email, salary, id, ))
        self.db.conn.commit()
        self.view_records()
        
    # удаление выделенных строк
    def delete_records(self):
        for row in self.tree.selection():
            self.db.cursor.execute('DELETE FROM personal WHERE id = ?',
                                (self.tree.set(row, '#1'), ))
        self.db.conn.commit()
        self.view_records()

    # метод вызывающий дочернее окно
    def open_child(self):
        Child()

    # метод вызывающий дочернее окно для редактирования данных
    def open_update_child(self):
        Update()

    # метод вызывающий дочернее окно для поиска данных
    def open_search(self):
        Search()

# класс дочернего окна
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app
    
    # инициализация виджетов дочернего окна
    def init_child(self):

        self.title('New')
        self.geometry('350x185')
        self.resizable(False, False)

        self.grab_set()
        self.focus_set()

        label_name = tk.Label(self, text='Name:')
        label_name.place(x=50, y=15)
        label_phone = tk.Label(self, text='Telephone:')
        label_phone.place(x=50, y=45)
        label_email = tk.Label(self, text='E-mail:')
        label_email.place(x=50, y=75)
        label_salary = tk.Label(self, text='Salary:')
        label_salary.place(x=50, y=105)

        self.entry_name = tk.Entry(self)
        self.entry_name.place(x=200, y=15)
        self.entry_phone = tk.Entry(self)
        self.entry_phone.place(x=200, y=45)
        self.entry_email = tk.Entry(self)
        self.entry_email.place(x=200, y=75)
        self.entry_salary = tk.Entry(self)
        self.entry_salary.place(x=200, y=105)

        btn_cancel = tk.Button(self, text='Close', command=self.destroy)
        btn_cancel.place(x=200, y=150)

        self.btn_add = tk.Button(self, text='Add')
        self.btn_add.bind('<Button-1>', lambda ev: self.view.records(self.entry_name.get(),
                                                                self.entry_phone.get(),
                                                                self.entry_email.get(),
                                                                self.entry_salary.get()))
        self.btn_add.place(x=265, y=150)

# класс дочернего окна для изменения данных
class Update(Child):

    def __init__(self):
        super().__init__()
        self.init_update()
        self.db = db
        self.default_data()

    def init_update(self):
        self.title('Update')
        self.btn_add.destroy()
        self.btn_upd = tk.Button(self, text='Update')
        self.btn_upd.bind('<Button-1>', 
                          lambda ev: self.view.update_record(self.entry_name.get(),
                                                             self.entry_phone.get(),
                                                             self.entry_email.get(),
                                                             self.entry_salary.get()))
        self.btn_upd.bind('<Button-1>', lambda ev: self.destroy(), add='+')
        self.btn_upd.place(x=265, y=150)

    def default_data(self):
        id = self.view.tree.set(self.view.tree.selection()[0], '#1')
        self.db.cursor.execute('SELECT * from personal WHERE id = ?', (id, ))
        row = self.db.cursor.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_phone.insert(0, row[2])
        self.entry_email.insert(0, row[3])

# класс окна для поиска
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app
    
    # инициализация виджетов дочернего окна
    def init_child(self):
        self.title('Search')
        self.geometry('450x100')
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()
        label_name = tk.Label(self, text='Name:')
        label_name.place(x=30, y=30)
        self.entry_name = tk.Entry(self)
        self.entry_name.place(x=130, y=30)
        btn_cancel = tk.Button(self, text='Close', command=self.destroy)
        btn_cancel.place(x=150, y=70)
        self.btn_add = tk.Button(self, text='Search')
        self.btn_add.bind('<Button-1>', 
                          lambda ev: self.view.search_records(self.entry_name.get()))
        self.btn_add.bind('<Button-1>', lambda ev: self.destroy(), add='+')
        self.btn_add.place(x=225, y=70)

# класс БД
class Db:
    def __init__(self):
        self.conn = sqlite3.connect('workers.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS personal (
                            id INTEGER PRIMARY KEY,
                            name TEXT,
                            phone TEXT,
                            email TEXT,
                            salary INTEGER
                        )''')
        self.conn.commit()

    # добавление данных в БД
    def insert_data(self, name, phone, email, salary):
        self.cursor.execute('''
                        INSERT INTO personal (name, phone, email, salary)
                        VALUES (?, ?, ?, ?)''', (name, phone, email, salary))
        self.conn.commit()



if __name__ == '__main__':
    root = tk.Tk()
    db = Db()
    app = Main(root)
    app.pack()
    root.title('DBWorkers')
    root.geometry('795x550')
    root.resizable(False, False)
    root.mainloop()