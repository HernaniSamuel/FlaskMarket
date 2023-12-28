from market.models import Item, User
from flask import render_template, Blueprint, redirect, url_for, flash, request
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
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
    form_sell = SellItemForm()

    if request.method == 'POST':
        purchased_item = request.form.get('purchased_item')
        p_item_obj = Item.query.filter_by(name=purchased_item).first()
        if p_item_obj:
            if p_item_obj.price > current_user.budget:
                flash("Budget not enough to complete purchase!", category='danger')
            else:
                p_item_obj.buy(current_user=current_user)
                flash(f"You bought { p_item_obj.name } for { p_item_obj.price }. Enjoy your product!", category='success')

        selled_item = request.form.get('selled_item')
        p_item_obj_sell = Item.query.filter_by(name=selled_item).first()
        if p_item_obj_sell:
            p_item_obj_sell.sell(current_user=current_user)
            flash('Produto vendido com sucesso!', category='success')


    items = Item.query.filter_by(owner=None)
    owned_items = Item.query.filter_by(owner=current_user.id)
    return render_template("market.html", items=items, current_user=current_user, formPurchase=form_purchase, formSell=form_sell, owned_items=owned_items)


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
        flash(f'Success! Welcome {user_to_create.username}!', category='success')
        return redirect(url_for('routes.market_page'))

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'Error in register: {err_msg}', category='danger')

    return render_template('register.html', form=form, current_user=current_user)


@routes.route("/login", methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('routes.market_page'))
        else:
            flash('Username and password are not match! Please try again', category='danger')

    return render_template('login.html', form=form, current_user=current_user)


@routes.route("/logout", methods=['GET', 'POST'])
@login_required
def logout_page():
    logout_user()
    flash('User disconnected successfully!', category='success')
    return redirect(url_for('routes.home_page'))
