import tkinter as tk
from tkinter import ttk


class Views:
    @staticmethod
    def create_modal(data, header):
        """
        This method allows make a modal when u use create frame
        :param data: data created
        :param header: header to table
        """
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
    def update_modal(id_, column):
        """
        This method allows make a modal when u use update frame
        :param id_: id_ updated
        :param column: column updated
        """
        modal = tk.Toplevel()
        modal.title("Success")

        label = tk.Label(modal, text=f"{column} {id_} updated")
        label.pack()

        ok_button = tk.Button(modal, text="OK", command=modal.destroy)
        ok_button.pack()

    @staticmethod
    def delete_modal(id_, column):
        """
        This method allows make a modal when u use update frame
        :param id_: id_ deleted
        :param column: column deleted
        """
        modal = tk.Toplevel()
        modal.title("Success")

        label = tk.Label(modal, text=f"{column} {id_} deleted")
        label.pack()

        ok_button = tk.Button(modal, text="OK", command=modal.destroy)
        ok_button.pack()

    @staticmethod
    def del_frame(cur_frame):
        """
        To delete the previous frames
        :param cur_frame: current frame
        """
        for frame in cur_frame.winfo_children():
            frame.destroy()

    def create_frame(self, cur_frame, crud, header, column):
        """
        This method allows make the frame to create data
        :param cur_frame: current frame
        :param crud: from class CRUD, that allows u to interact with the database
        :param header: values to datatable
        :param column: table
        :return:
        """
        self.del_frame(cur_frame)

        dict_values = {key: tk.StringVar() for key in header.split(", ")}
        for key, var in dict_values.items():
            lb = tk.Label(cur_frame, text=key)
            lb.pack()
            en = tk.Entry(cur_frame, textvariable=var)
            en.pack()

        def clear_entry():
            """
            To clear each entry
            """
            for v in dict_values.values():
                v.set("")

        def create():
            """
            To finish the creation
            """
            data = [v.get() for v in dict_values.values()]

            if crud.create(column, header, data):
                self.create_modal(data, header)
                clear_entry()

        btn = tk.Button(cur_frame, text="Confirm to Create", command=create)
        btn.pack()

    def read_frame(self, cur_frame, crud, keys, header, column):
        """
        This method allows make the frame to read data
        :param cur_frame: current frame
        :param crud: from class CRUD, that allows u to interact with the database
        :param keys: keys to class
        :param header: values to datatable
        :param column: table
        """
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
        """
        This method allows make the frame to update data
        :param cur_frame: current frame
        :param crud: from class CRUD, that allows u to interact with the database
        :param header: values to datatable
        :param column: table
        """
        self.del_frame(cur_frame)

        id_ = tk.IntVar()
        lb_id = tk.Label(cur_frame, text="ID to search")
        lb_id.pack()
        en_id = tk.Entry(cur_frame, textvariable=id_)
        en_id.pack()

        btn_id = tk.Button(cur_frame, text="Search", command=lambda: get_data())
        btn_id.pack()

        show_frame = tk.Frame(cur_frame)
        show_frame.pack()

        dict_values = {key: tk.StringVar() for key in header.split(", ")}
        for key, var in dict_values.items():
            lb = tk.Label(cur_frame, text=key)
            lb.pack()
            en = tk.Entry(cur_frame, textvariable=var)
            en.pack()

        def get_data():
            """
            :param _id: ID to search
            """
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
            """
            To clear each entry
            """
            for v in dict_values.values():
                v.set("")

            id_.set(0)

        def update_():
            """
            To finish the update
            :return:
            """
            data = [v.get() for v in dict_values.values()]

            if crud.update_(column, header.split(', '), id_.get(), data):
                self.update_modal(id_.get(), column)
                clear_entry()

        btn = tk.Button(cur_frame, text="Confirm to Update", command=update_)
        btn.pack()

    def delete_frame(self, cur_frame, crud, model, column):
        """
        This method allows make the frame to delete data
        :param cur_frame: current frame
        :param crud: from class CRUD, that allows u to interact with the database
        :param model: object to delete
        :param column: table
        """
        self.del_frame(cur_frame)

        id_ = tk.IntVar()
        lb_id = tk.Label(cur_frame, text="ID to search")
        lb_id.pack()
        en_id = tk.Entry(cur_frame, textvariable=id_)
        en_id.pack()

        btn_id = tk.Button(cur_frame, text="Search", command=lambda: get_data())
        btn_id.pack()

        show_frame = tk.Frame(cur_frame)
        show_frame.pack()

        def get_data():
            """
            To search data
            :return:
            """
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

        def clear():
            """
            To clear the show frame
            """
            self.del_frame(show_frame)
            id_.set(0)

        def delete_():
            """
            To finish the removal
            """
            if crud.delete_(column, id_.get()):
                self.delete_modal(id_.get(), column)
                clear()

        btn = tk.Button(cur_frame, text="Confirm to Delete", command=delete_)
        btn.pack()
