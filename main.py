from crud import CRUD
from models import Product, Client, Shop, Detail
from controller import Controller
import tkinter as tk

crud = CRUD("db_test")

root = tk.Tk()
root.geometry("1000x600")
root.title("Shop")
option_frame = tk.Frame(root, bg="#bcbcbc")
option_frame.pack(side=tk.LEFT)
option_frame.pack_propagate(False)
option_frame.configure(height=1000, width=200)

main_frame = tk.Frame(root, highlightbackground='black', highlightthickness=1)
main_frame.pack(side=tk.LEFT, expand=True, fill="both")
main_frame.pack_propagate(False)
main_frame.configure(height=1000, width=800)

crud.init_db()

controller = Controller()

controller.make_frame(Product(), "product", crud, option_frame, main_frame)
controller.make_frame(Client(), "client", crud, option_frame, main_frame)
controller.make_frame(Shop(), "shop", crud, option_frame, main_frame,
                      [[Client(), "client"]])
controller.make_frame(Detail(), "detail", crud, option_frame, main_frame,
                      [[Shop(), "shop"], [Product(), "product"]])



root.mainloop()
