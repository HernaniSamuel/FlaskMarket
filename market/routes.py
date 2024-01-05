from market.models import Item, User
from flask import render_template, Blueprint, redirect, url_for, flash, request
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm, AdicionaForm
from . import db
from flask_login import login_user, current_user, logout_user, login_required

routes = Blueprint('routes', __name__)


@routes.route('/')
def home_page():
    return render_template('index.html', current_user=current_user)


@routes.route("/market", methods=['GET', 'POST'])
@login_required
def market_page():
    form_purchase = PurchaseItemForm()

    if request.method == 'POST':
        purchased_item = request.form.get('purchased_item')
        p_item_obj = Item.query.filter_by(name=purchased_item).first()
        if p_item_obj:
            if p_item_obj.price > current_user.budget:
                flash("Dinheiro em conta insuficiente!", category='danger')
            else:
                p_item_obj.buy(current_user=current_user)
                flash(f"Você comprou { p_item_obj.name } por { p_item_obj.price }. Aproveite seu produto!", category='success')

    items = Item.query.filter_by(owner=None)
    return render_template("market.html", items=items, current_user=current_user, formPurchase=form_purchase)


@routes.route("/owner", methods=['GET', 'POST'])
@login_required
def owner_page():
    form_sell = SellItemForm()

    if request.method == "POST":
        sold_item = request.form.get('sold_item')
        p_item_obj_sell = Item.query.filter_by(name=sold_item).first()
        if p_item_obj_sell:
            p_item_obj_sell.sell(current_user=current_user)
            flash('Produto vendido com sucesso!', category='success')

    owned_items = Item.query.filter_by(owner=current_user.id)
    return render_template("owner.html", current_user=current_user, formSell=form_sell, owned_items=owned_items)


@routes.route("/register", methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)

        db.session.add(user_to_create)
        db.session.commit()

        login_user(user_to_create)
        flash(f'Sucesso! Bem-vindo(a) {user_to_create.username}!', category='success')
        return redirect(url_for('routes.market_page'))

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'Erro ao registrar: {err_msg}', category='danger')

    return render_template('register.html', form=form, current_user=current_user)


@routes.route("/adicionar-saldo", methods=['GET', 'POST'])
@login_required
def adicionar_saldo_page():
    adiciona_form = AdicionaForm()

    if request.method == 'POST':
        valor_adicao = request.form.get('quantia')
        try:
            current_user.budget += float(valor_adicao)
            db.session.commit()
            return redirect(url_for('routes.market_page'))
        except:
            flash("Erro ao adicionar quantia! Vírgulas ou letras não são aceitas! Coloque . em vez de ,", category='danger')

    return render_template('adiciona.html', current_user=current_user, form=adiciona_form)

@routes.route("/login", methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Sucesso! Você entrou como: {attempted_user.username}', category='success')
            return redirect(url_for('routes.market_page'))
        else:
            flash('Nome e senha não condizem!', category='danger')

    return render_template('login.html', form=form, current_user=current_user)


@routes.route("/logout", methods=['GET', 'POST'])
@login_required
def logout_page():
    logout_user()
    flash('Desconectado com sucesso!', category='success')
    return redirect(url_for('routes.home_page'))
