from market.models import Item, db
from market import create_app
app = create_app()


def add_product():
    with app.app_context():
        print("Enter product details to add it to the database.")
        name = input("Product Name: ")
        price = int(input("Price: "))
        barcode = input("Barcode: ")
        description = input("Description: ")

        new_item = Item(name=name, price=price, barcode=barcode, description=description)
        db.session.add(new_item)
        db.session.commit()
        print(f"Product '{name}' added successfully!")


if __name__ == "__main__":
    add_product()

# Criado pelo ChatGPT-4 da OpenAI
