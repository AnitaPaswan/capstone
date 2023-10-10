from datetime import datetime
from flask_wtf import FlaskForm as Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, AnyOf, URL
import re
from enums import Gender


gender_choices = [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
]
def isValidAge(number):
    regex = re.compile('([0-9]){2}')
    return regex.match(number)

class ActorForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    age = StringField(
        'age', validators=[DataRequired()]
    )
    gender = SelectMultipleField(
        'gender', validators=[DataRequired()],
        choices=Gender.choices()
     )
    def validate(self, **kwargs):
        validated = Form.validate(self)
        if not validated:
            return False
        if not isValidAge(self.age.data):
            self.age.errors.append('Invalid Age. Age should be numeric.')
            return False
        if not set(self.gender.data).issubset(dict(Gender.choices()).keys()):
            self.gender.errors.append('Invalid gender.')
            return False
        return True
    


