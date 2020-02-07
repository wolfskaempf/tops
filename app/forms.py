from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, TextAreaField
from wtforms.validators import DataRequired, Optional


class CreateTopForm(FlaskForm):
    titel = StringField('Titel', validators=[DataRequired()])
    eingereicht_von = StringField('Eingereicht von', validators=[DataRequired()])
    frist = DateField('Frist', format=("%d.%m.%Y"), validators=[Optional()])
    beschreibung = TextAreaField('Beschreibung')
    abstimmungsfragen = TextAreaField('Abstimungsfragen')
    submit = SubmitField('Einreichen')


class LoginForm(FlaskForm):
    management_password = StringField('Passwort', validators=[DataRequired()])
    submit = SubmitField('Autorisierungstoken setzen')
