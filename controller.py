import tkinter as tk
from views import Views


class Controller:
    def __init__(self):
        self.view = Views()

    def model_page(self, cur_frame, crud, model, column, objs_to_show: [] = None):
        """
        This method is the root of all, that allows make just with the object all frames
        :param cur_frame: current frame
        :param crud: from class CRUD, that allows u to interact with the database
        :param model: object
        :param column: table
        :param objs_to_show: if u want display more objects
        :return:
        """
        for frame in cur_frame.winfo_children():
            frame.destroy()

        lb = tk.Label(cur_frame, text=f"{column} Page", font=("Bold", 30))
        lb.pack()

        opt_frame = tk.Frame(cur_frame)
        opt_frame.pack()

        form_frame = tk.Frame(cur_frame)
        form_frame.pack()

        btn_create = tk.Button(opt_frame, text="Create",
                               command=lambda: self.view.create_frame(form_frame, crud,
                                                                      model.get_keys_without_id_str, column))
        btn_create.pack()

        btn_read = tk.Button(opt_frame, text=f"Read",
                             command=lambda: self.view.read_frame(form_frame, crud, model.get_keys_str(), "*", column))
        btn_read.pack()

        btn_update = tk.Button(opt_frame, text="Update",
                               command=lambda: self.view.update_frame(form_frame, crud, model.columns_to_upd(), column))
        btn_update.pack()

        btn_delete = tk.Button(opt_frame, text="Delete",
                               command=lambda: self.view.delete_frame(form_frame, crud, model, column))
        btn_delete.pack()

        if objs_to_show:
            for _model, _column in objs_to_show:
                btn_more = tk.Button(opt_frame, text=f"Read {_column}",
                                     command=lambda mod=_model, col=_column:
                                     self.view.read_frame(form_frame, crud, mod.get_keys_str(), "*", col))
                btn_more.pack()

    def make_frame(self, model, column, crud, option_frame, main_frame, data_show: [] = None):
        """
        This method allows u to make frame button to access each object
        :param model: base object
        :param column: table
        :param crud: from class CRUD, that allows u to interact with the database
        :param option_frame: where the buttons will be
        :param main_frame: where the rest will be
        :param data_show: other objects u want to display
        """
        btn_option = tk.Button(option_frame, text=column,
                               command=lambda: self.model_page(main_frame, crud, model, column, data_show))
        btn_option.pack()
