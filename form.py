from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError, Email
from flask_bcrypt import Bcrypt
from tables import User
from abc import ABC, abstractmethod

bcrypt = Bcrypt()

# --- Products
class Form(FlaskForm):
    pass

class SignupForm(Form):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "e.g. NewsReader99"})
    
    email = StringField(validators=[
                        InputRequired(), Email(), Length(max=50)], render_kw={"placeholder": "name@example.com"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "••••••••"})

    submit = SubmitField('Sign Up')

    def validate_username(self, username): 
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')

    def validate_email(self, email):
        existing_user_email = User.query.filter_by(
            email=email.data).first()
        if existing_user_email:
            raise ValidationError(
                'That email is already registered.')
class LoginForm(Form):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if not user:
            raise ValidationError("Username doesn't exist.")

    def validate_password(self, password):
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            if not bcrypt.check_password_hash(user.password, password.data):
                raise ValidationError("Incorrect password.")  
#Abstract fact
class FormFactory(ABC):
    @abstractmethod
    def create_form(self):
        pass

# Concrete Fact
class LoginFormFactory(FormFactory):
    def create_form(self):
        return LoginForm()

class SignupFormFactory(FormFactory):
    def create_form(self):
        return SignupForm()

# Singleton Factory Registry
class FactoryRegistry:
    _instance = None 
    _factories = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FactoryRegistry, cls).__new__(cls)
        return cls._instance
  
    def register_factory(self, form_type, factory: FormFactory):
        """Registers a factory instance under a specific key."""
        self._factories[form_type] = factory
        
    def get_factory(self, form_type) -> FormFactory:
        """Retrieves the factory associated with the form_type."""
        return self._factories.get(form_type)

registry = FactoryRegistry()
registry.register_factory('login', LoginFormFactory())
registry.register_factory('signup', SignupFormFactory())