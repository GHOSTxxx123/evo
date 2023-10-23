from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField, BooleanField, PasswordField, SelectField, MultipleFileField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError, Email
from app.model import Compani, User



class Sign_in(FlaskForm):
    user = StringField('Login', validators=[DataRequired(),
                                             Length(min=2, max=100)])
    password = PasswordField('Пароль', validators=[DataRequired(),
                                             Length(min=8, max=100)])
    remember = BooleanField("Запомнить меня")                                        
    submit = SubmitField('Вход')         


class Sign_up(FlaskForm):
    user = StringField('Login', validators=[DataRequired(),
                                             Length(min=2, max=100)])                                        
    password = PasswordField('Пароль', validators=[DataRequired(),
                                             Length(min=8, max=100)])                                                                               

    submit = SubmitField('Авторизация')                                             
    
    def validate_gmail(self, name):
        name = User.query.filter_by(user_name=name.data).first()
        if name:
            raise ValidationError('Такой пользователь уже существует !!!')

class Create_Compani(FlaskForm):

    campaning_name = StringField('Название кампании', validators=[DataRequired(),
                                             Length(min=2, max=200)])
    status = SelectField('Выбор приложении', choices=[('start', 'start'), ('stop', 'stop'), ('pause', 'pause'), 
                                ('schedule', 'schedule')])
    
    license_in_use = IntegerField('Количество лицензий', validators=[NumberRange(min=1, max=1000)])

    file = FileField('', validators=[DataRequired(), FileAllowed(['txt'])])
    
    submit = SubmitField('Создать') 

    def validate_full_name(self, campaning_name):
        campaning_name = Compani.query.filter(Compani.Campaning_Name == campaning_name.data).first()
        if campaning_name:
            raise ValidationError('Такой продукт уже создан !!!')


class Edit_Compani(FlaskForm):
    campaning_name = StringField('Название кампании', validators=[DataRequired(),
                                             Length(min=2, max=200)])
    status = SelectField('Status', choices=[('start', 'start'), ('stop', 'stop'), ('pause', 'pause'), 
                                ('schedule', 'schedule')])
    
    license_in_use = IntegerField('Количество лицензий', validators=[NumberRange(min=1, max=1000)])
    
    collection_pointer = IntegerField('Collection Pointer', validators=[NumberRange(min=1, max=100000000)])
    
    attempts = IntegerField('Attempts', validators=[NumberRange(min=1, max=100000000)])
    
    first_call_time = IntegerField('First call time', validators=[NumberRange(min=1, max=100000000)])
    
    last_call_time = IntegerField('Last call time', validators=[NumberRange(min=1, max=100000000)])
    
    buffer_pointer = IntegerField('Buffer pointer', validators=[NumberRange(min=1, max=100000000)])
    
    submit = SubmitField('Создать') 

    def validate_full_name(self, campaning_name):
        campaning_name = Compani.query.filter(Compani.Campaning_Name == campaning_name.data).first()
        if campaning_name:
            raise ValidationError('Такой продукт уже создан !!!')

