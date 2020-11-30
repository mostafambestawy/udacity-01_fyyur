from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField
from wtforms.fields import BooleanField,TextAreaField
from wtforms.validators import DataRequired, AnyOf, URL


states = [
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]
genres=[
            ('Alternative', 'Alternative'),
            ('Blues', 'Blues'),
            ('Classical', 'Classical'),
            ('Country', 'Country'),
            ('Electronic', 'Electronic'),
            ('Folk', 'Folk'),
            ('Funk', 'Funk'),
            ('Hip-Hop', 'Hip-Hop'),
            ('Heavy Metal', 'Heavy Metal'),
            ('Instrumental', 'Instrumental'),
            ('Jazz', 'Jazz'),
            ('Musical Theatre', 'Musical Theatre'),
            ('Pop', 'Pop'),
            ('Punk', 'Punk'),
            ('R&B', 'R&B'),
            ('Reggae', 'Reggae'),
            ('Rock n Roll', 'Rock n Roll'),
            ('Soul', 'Soul'),
            ('Other', 'Other'),
        ]

class ShowForm(Form):
    artist_id = StringField(
        'artist_id'
    )
    venue_id = StringField(
        'venue_id'
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default= datetime.today()
    )

class VenueForm(Form):
    def __init__(self, obj, *args, **kwargs):
        super(VenueForm, self).__init__(*args, **kwargs)
        self.state.data = obj.state
        self.genres.data =str(obj.genres).split(",")
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=states
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )
    phone = StringField(
        'phone'
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction
        'genres', validators=[DataRequired()],
        choices=genres,
        coerce=genres
        
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL(message="facebook link not valid URL")]
    )
    website = StringField(
        # TODO implement enum restriction
        'website',validators=[URL(message="website not valid URL")]
    )
    seeking_talent=BooleanField('seeking_talent',)
    seeking_description=TextAreaField('seeking_description',
    render_kw={'class': 'form-control', 'rows': 3}
    )

class NewVenueForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=states
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )
    phone = StringField(
        'phone'
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction
        'genres', validators=[DataRequired()],
        choices=genres,
        coerce=genres
        
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL(message="facebook link not valid URL")]
    )
    website = StringField(
        # TODO implement enum restriction
        'website', validators=[URL(message="website not valid URL")]
    )
    seeking_talent=BooleanField('seeking_talent',)
    seeking_description=TextAreaField('seeking_description',
    render_kw={'class': 'form-control', 'rows': 3}
    )
    

class ArtistForm(Form):
    def __init__(self, obj, *args, **kwargs):
        super(ArtistForm, self).__init__(*args, **kwargs)
        self.state.data = obj.state
        self.genres.data =str(obj.genres).split(",")
    name = StringField(
        'name', validators=[DataRequired()],
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=states
    )
    phone = StringField(
        # TODO implement validation logic for state
        'phone'
    )
    
    genres = SelectMultipleField(
        # TODO implement enum restriction
        'genres', validators=[DataRequired()],
        choices=genres,
        coerce=genres
    )
    image_link = StringField(
        'image_link',
        
    )
    facebook_link = StringField(
        # TODO implement enum restriction
        'facebook_link', validators=[URL(message="facebook link not valid URL")]
    )

# TODO IMPLEMENT NEW ARTIST FORM AND NEW SHOW FORM

class NewArtistForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=states
    )
    phone = StringField(
        # TODO implement validation logic for state
        'phone'
        
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction
        'genres', validators=[DataRequired(message="select one genre at least")],
        choices=genres,
        coerce=genres
    )
    image_link = StringField(
        'image_link',
        
    )
    website = StringField(
        # TODO implement enum restriction
        'website', validators=[URL(message="website not valid URL")]
    )
    facebook_link = StringField(
        # TODO implement enum restriction
        'facebook_link', validators=[URL(message="facebook link not valid URL")]
    )
    seeking_venue=BooleanField('seeking_venue',)
    seeking_description=TextAreaField('seeking_description',
    render_kw={'class': 'form-control', 'rows': 3}
    )


