from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from .models import User


class RegisterForm(FlaskForm):

    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError("Nome de usuário já em uso, por favor escolha outro nome!")

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError("Endereço de email já em uso, por favor, tente outro endereço de email!")


    username = StringField(label='Nome', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='E-mail', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Senha', validators=[Length(min=6, max=16), DataRequired()])
    password2 = PasswordField(label='Confirmar senha', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Criar conta!')


class LoginForm(FlaskForm):
    username = StringField(label='Nome', validators=[DataRequired()])
    password = StringField(label='Senha', validators=[DataRequired()])
    submit = SubmitField(label='Entrar!')


class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label='Comprar agora!')


class SellItemForm(FlaskForm):
    submit = SubmitField(label='Vender agora!')
