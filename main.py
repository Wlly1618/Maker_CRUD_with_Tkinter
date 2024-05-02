from crud import CRUD
from models import Product

crud = CRUD("db_test_2")
crud.init_db()


def show(p):
    print(f"ID: {p.id}\t\t"
          f"Name: {p.name}\t\t"
          f"Price: {p.price}\t\t"
          f"Stock: {p.stock}\t\t")


# p_1 = Product.create(name="ll", price=10.99, stock=50)
# show(p_1)

# p_2 = Product.get_by_id(_id=13)
# show(p_2)

print("")
p_get = Product.get()
for item in p_get:
    show(item)
