from wtforms import Form, StringField, RadioField, SelectField, DecimalField, TextAreaField, validators, ValidationError
from wtforms.fields import EmailField, DateField

def validate_date_format(form, field):
    date = field.data
    if not date:
        return
    try:
        month, year = date.split('/')
        if not (1 <= int(month) <= 12):
            raise ValidationError("Month must be between 01 and 12.")
    except ValueError:
        raise ValidationError("Invalid date format. Must be MM/YY.")
    
class PaymentForm(Form):
    paymentMethod= RadioField('Payment Method:', choices=[('Visa', 'Visa'), ('Mastercard', 'Mastercard'), ('PayNow', 'PayNow'), ], default='Visa')
    creditcard = StringField('Credit Card Number:', [validators.Length(min=16, max=16), validators.Regexp(r'^\d+$', message="Credit card number must contain only numbers."), validators.DataRequired()])
    date = StringField('Date (MM/YY):', [validators.Length(min=5, max=5),validators.Regexp(r'^\d{2}/\d{2}$', message="Date must be in MM/YY format."),validate_date_format, validators.DataRequired()])
    cvv = StringField('CVV:',[validators.Length(min=3, max=3),validators.Regexp(r'^\d+$', message="CVV must contain only numbers."),validators.DataRequired()])
    name = StringField('Name on Card:', [validators.Length(min=1, max=20), validators.DataRequired()])

class DonationForm(Form):
    society = SelectField('Donate to', [validators.DataRequired()],choices=[
            ('Singapore Green Plan 2030', 'Singapore Green Plan 2030'),
            ('HDB Green Towns Programme', 'HDB Green Towns Programme'),
            ('National Recycling Programme (NRP)', 'National Recycling Programme (NRP)'),
            ('NEWater','NEWater'),
            ('OneMillionTrees Movement','OneMillionTrees Movement'),
            ('Walk Cycle Ride SG Programme','Walk Cycle Ride SG Programme'),
            ('Agri-Food Cluster Transformation Fund (ACT Fund)','Agri-Food Cluster Transformation Fund (ACT Fund)'),
            ('Zero Waste Masterplan','Zero Waste Masterplan'),
            ('National Hydrogen Strategy','National Hydrogen Strategy')
        ]
    )
    creditcard = StringField('Credit Card Number:', [validators.Length(min=16, max=16), validators.Regexp(r'^\d+$', message="Credit card number must contain only numbers."), validators.DataRequired()])
    date = StringField('Date (MM/YY):', [validators.Length(min=5, max=5),validators.Regexp(r'^\d{2}/\d{2}$', message="Date must be in MM/YY format."),validate_date_format, validators.DataRequired()])
    cvv = StringField('CVV:',[validators.Length(min=3, max=3),validators.Regexp(r'^\d+$', message="CVV must contain only numbers."),validators.DataRequired()])
    name = StringField('Name on Card:', [validators.Length(min=1, max=20), validators.DataRequired()])
    donateamt = DecimalField('Amount to donate:', [validators.NumberRange(min=1, message="The minimum donation amount is $1."), validators.DataRequired()])

class DetailForm(Form):
    accountname = StringField('Account Name:', [validators.Length(min=1, max=16), validators.DataRequired()])
    accountid = StringField('Account ID:', [validators.Length(min=1, max=10)])
    doc = StringField('Date-of-Creation:', [validators.DataRequired(), validators.Length(min=1,)])
    accountemail = EmailField('Account Email:', [validators.Length(min=1, max=100), validators.DataRequired()])

class CreateSubForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired() ], render_kw={"placeholder": "E.g. John", "class": "form-control"} )
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()], render_kw={"placeholder": "E.g. Toel", "class": "form-control"})
    gender = SelectField('Gender', [validators.DataRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    email = EmailField('Email', [validators.Email(), validators.DataRequired()], render_kw={"placeholder": "E.g. Johntoel@gmail.com", "class": "form-control"} )
    remarks = TextAreaField('Remarks', [validators.Optional()], render_kw={"placeholder": "E.g. Anything you wish to tell us...", "class": "form-control"})

