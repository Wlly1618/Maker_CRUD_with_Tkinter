import tkinter as tk
from tkinter import ttk


class BaseEntity:
    def get_keys_str(self):
        return ', '.join(map(str, vars(self).keys()))

    def get_values_str(self):
        return ', '.join(map(str, vars(self).values()))

    def get_values_array(self):
        return list(vars(self).values())

    @property
    def get_keys_without_id_str(self):
        keys = vars(self).keys()
        keys_without_id = [key for key in keys if key != '_id']
        return ', '.join(map(str, keys_without_id))

    @staticmethod
    def update_modal(id_, column):
        modal = tk.Toplevel()
        modal.title("Success")

        label = tk.Label(modal, text=f"{column} {id_} updated")
        label.pack()

        ok_button = tk.Button(modal, text="OK", command=modal.destroy)
        ok_button.pack()

    @staticmethod
    def create_modal(data, header):
        modal = tk.Toplevel()
        modal.title("Success")
        modal.geometry("200x200")

        message = f"Product created.\nData:\n"
        for i, value in enumerate(data):
            message += f"{header.split()[i]}: {value}\n"

        label = tk.Label(modal, text=message)
        label.pack()

        ok_button = tk.Button(modal, text="OK", command=modal.destroy)
        ok_button.pack()

    @staticmethod
    def del_frame(cur_frame):
        for frame in cur_frame.winfo_children():
            frame.destroy()

    def create_frame(self, cur_frame, crud, header, column):
        self.del_frame(cur_frame)

        dict_values = {key: tk.StringVar() for key in header.split(", ")}
        for key, var in dict_values.items():
            lb = tk.Label(cur_frame, text=key)
            lb.pack()
            en = tk.Entry(cur_frame, textvariable=var)
            en.pack()

        def clear_entry():
            for v in dict_values.values():
                v.set("")

        def create():
            data = [v.get() for v in dict_values.values()]

            if crud.create(column, header, data):
                self.create_modal(data, header)
                clear_entry()

        btn = tk.Button(cur_frame, text="Confirm to Create", command=create)
        btn.pack()

    def read_frame(self, cur_frame, crud, keys, header, column):
        self.del_frame(cur_frame)
        tree = ttk.Treeview(cur_frame)
        keys = keys.split(", ")
        tree["columns"] = keys

        for key in keys:
            tree.heading(key, text=key)

        data = crud.read(column, header)
        for item in data:
            tree.insert("", "end", values=item)

        tree.pack(expand=True, fill="both")

    def update_frame(self, cur_frame, crud, header, column):
        self.del_frame(cur_frame)

        id_ = tk.IntVar()
        lb_id = tk.Label(cur_frame, text="ID to search")
        lb_id.pack()
        en_id = tk.Entry(cur_frame, textvariable=id_)
        en_id.pack()

        btn_id = tk.Button(cur_frame, text="Search", command=lambda: get_data(id_))
        btn_id.pack()

        show_frame = tk.Frame(cur_frame)
        show_frame.pack()

        dict_values = {key: tk.StringVar() for key in header.split(", ")}
        for key, var in dict_values.items():
            lb = tk.Label(cur_frame, text=key)
            lb.pack()
            en = tk.Entry(cur_frame, textvariable=var)
            en.pack()

        def get_data(_id):
            self.del_frame(show_frame)
            data = crud.read_with_id(id_.get(), header, column)

            if data is not None or data != 1:
                for item in data:
                    for value, key in zip(item, dict_values.values()):
                        key.set(value)
            else:
                lb_data = tk.Label(show_frame, text="No data found")
                lb_data.pack()

        def clear_entry():
            for v in dict_values.values():
                v.set("")

        def update_():
            data = [v.get() for v in dict_values.values()]

            if crud.update_(column, header.split(', '), id_.get(), data):
                self.update_modal(id_.get(), column)
                clear_entry()

        btn = tk.Button(cur_frame, text="Confirm to Update", command=update_)
        btn.pack()

    def delete_frame(self, cur_frame, crud, model, column):
        self.del_frame(cur_frame)

        id_ = tk.IntVar()
        lb_id = tk.Label(cur_frame, text="ID to search")
        lb_id.pack()
        en_id = tk.Entry(cur_frame, textvariable=id_)
        en_id.pack()

        btn_id = tk.Button(cur_frame, text="Search", command=lambda: get_data(id_))
        btn_id.pack()

        show_frame = tk.Frame(cur_frame)
        show_frame.pack()

        def get_data(_id):
            self.del_frame(show_frame)

            data = crud.read_with_id(id_.get(), model.get_keys_without_id_str, column)

            if data is not None or data != 1:
                for item in data:
                    for value in item:
                        lb_data = tk.Label(show_frame, text=value)
                        lb_data.pack()
            else:
                lb_data = tk.Label(show_frame, text="No data found")
                lb_data.pack()

        def clear_entry():
            self.del_frame(show_frame)

        def delete_():
            if crud.delete_(column, id_.get()):
                self.update_modal(id_.get(), column)
                clear_entry()

        btn = tk.Button(cur_frame, text="Confirm to Delete", command=delete_)
        btn.pack()

    def model_page(self, cur_frame, crud, model, column, objs_to_show: [] = None):
        model_frame = tk.Frame(cur_frame)
        model_frame.pack(pady=20, expand=True, fill="both")

        lb = tk.Label(model_frame, text=f"{column} Page", font=("Bold", 30))
        lb.pack()

        opt_frame = tk.Frame(model_frame)
        opt_frame.pack()

        form_frame = tk.Frame(model_frame)
        form_frame.pack()

        btn_create = tk.Button(opt_frame, text="Create",
                               command=lambda: self.create_frame(form_frame, crud,
                                                                 model.get_keys_without_id_str, column))
        btn_create.pack()

        btn_read = tk.Button(opt_frame, text=f"Read",
                             command=lambda: self.read_frame(form_frame, crud, model.get_keys_str(), "*", column))
        btn_read.pack()

        btn_update = tk.Button(opt_frame, text="Update",
                               command=lambda: self.update_frame(form_frame, crud, model.columns_to_upd(), column))
        btn_update.pack()

        btn_delete = tk.Button(opt_frame, text="Delete",
                               command=lambda: self.delete_frame(form_frame, crud, model, column))
        btn_delete.pack()

        if objs_to_show:
            for _model, _column in objs_to_show:
                btn_more = tk.Button(opt_frame, text=f"Read {_column}",
                                     command=lambda mod=_model, col=_column:
                                     self.read_frame(form_frame, crud, mod.get_keys_str(), "*", col))
                btn_more.pack()

    @staticmethod
    def run(page, cur_frame, crud, model, column, objs_to_show: []):
        for frame in cur_frame.winfo_children():
            frame.destroy()

        page(cur_frame, crud, model, column, objs_to_show)

    def make_frame(self, model, column, crud, option_frame, main_frame, data_show: [] = None):
        btn_option = tk.Button(option_frame, text=column,
                               command=lambda: self.run(self.model_page, main_frame, crud, model, column, data_show))
        btn_option.pack()


class Product(BaseEntity):
    def __init__(self, _id=0, name="", price=0.0, stock=100):
        self._id = _id
        self.name = name
        self.price = price
        self.stock = stock

    @staticmethod
    def columns_to_upd():
        return "name, price, stock"


class Client(BaseEntity):
    def __init__(self, _id=0, name=""):
        self._id = _id
        self.name = name

    @staticmethod
    def columns_to_upd():
        return "name"


class Shop(BaseEntity):
    def __init__(self, _id=0, id_client="", date_time=""):
        self._id = _id
        self.id_client = id_client
        self.date = date_time

    @staticmethod
    def columns_to_upd():
        return ""


class Detail(BaseEntity):
    def __init__(self, _id=0, id_shop="", id_product="", amount=""):
        self._id = _id
        self.id_shop = id_shop
        self.id_product = id_product
        self.amount = amount

    @staticmethod
    def columns_to_upd():
        return "id_product, amount"
