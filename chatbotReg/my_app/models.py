from django.db import models

from mongoengine import Document, StringField, DateTimeField, EmbeddedDocument, EmbeddedDocumentField, IntField, BooleanField, ListField
from datetime import datetime

class TravelRequirements(EmbeddedDocument):
    transport_mode = StringField()
    arrival_location = StringField()

class Accommodation(EmbeddedDocument):
    type = StringField()
    number_of_people = IntField()

class Bhandara(Document):
    full_name = StringField(required=True)
    abhyasi_id = StringField(required=True, unique=True)
    email = StringField(required=True)
    phone = StringField(required=True)
    age = StringField(required=True)
    registration_timestamp = DateTimeField(default=datetime.utcnow)
    arrival_date = StringField()
    departure_date = StringField()
    travel_requirements = EmbeddedDocumentField(TravelRequirements)
    accommodation = EmbeddedDocumentField(Accommodation)

    meta = {'collection': 'bhandara'}


class AccommodationDetails(EmbeddedDocument):
    type = StringField()
    number_of_people = IntField()

class Gitopadesh(Document):
    full_name = StringField(required=True)
    abhyasi_id = StringField(required=True,unique=True)
    registration_timestamp = DateTimeField(default=datetime.utcnow)
    arrival_date = StringField()
    language_preference = StringField()
    accommodation = EmbeddedDocumentField(AccommodationDetails)

    meta = {'collection': 'gitopadesh'}


class Hope(Document):
    full_name = StringField(required=True)
    abhyasi_id = StringField(required=True,unique=True)
    registration_timestamp = DateTimeField(default=datetime.utcnow)
    batch_date = StringField()
    experience_level = StringField()
    accommodation = EmbeddedDocumentField(AccommodationDetails)

    meta = {'collection': 'hope'}