from market.models import Item, db
from market import create_app
app = create_app()


def add_product():
    with app.app_context():
        print("Coloque os detalhes o produto para adiciona-lo ao banco de dados!")
        name = input("Nome: ")
        price = int(input("Preço: "))
        barcode = input("Código de barras: ")
        description = input("Descrição: ")

        new_item = Item(name=name, price=price, barcode=barcode, description=description)
        db.session.add(new_item)
        db.session.commit()
        print(f"Product '{name}' adicionado com sucesso!")


if __name__ == "__main__":
    add_product()

# Criado pelo ChatGPT-4 da OpenAI
