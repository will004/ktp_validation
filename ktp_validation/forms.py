from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

import re

class RecognitionForm(FlaskForm):
    ktp = FileField('KTP', validators=[DataRequired(), FileAllowed(['jpg', 'png', 'jpeg'])])

    name = StringField('Name', validators=[
        DataRequired()
    ])

    nik = StringField('NIK', validators=[
        DataRequired(), Length(16,16)
    ])

    dob = StringField('Date Of Birth', validators=[
        DataRequired()
    ])

    submit = SubmitField('Validate')

    def validate_nik(self, nik):
        if not str(nik.data).isdigit():
            raise ValidationError('NIK must be in number')
    
    def validate_dob(self, dob):
        if not re.match('^(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d$', str(dob.data)):
            raise ValidationError('DOB must be dd/mm/yyyy')