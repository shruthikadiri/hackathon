from datetime import datetime

from django.shortcuts import render

# Create your views here.

import random
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Bhandara, TravelRequirements, Accommodation, Gitopadesh, AccommodationDetails, Hope
from mongoengine.errors import NotUniqueError

from django.shortcuts import render


# Define a list of greetings
greetings_list = [
    "Hi there!",
    "Hello! How can I assist you?",
    "Good day! Need any help?",
    "Greetings! How are you doing today?",
    "Hey! What can I do for you?",
    "Welcome! How can I be of service?"
]

@api_view(['GET'])
def random_greeting(request):
    random_message = random.choice(greetings_list)
    return Response({"greeting": random_message})


@api_view(['POST'])
def register_bhandara(request):
    try:
        data = request.data

        # Extract fields from the request
        travel_data = data.get('travel_requirements', {})
        accommodation_data = data.get('accommodation', {})

        # Create and save the Bhandara document
        bhandara_entry = Bhandara(
            full_name=data.get('full_name'),
            email=data.get('email'),
            phone=data.get('phone'),
            age=data.get('age'),
            abhyasi_id=data.get('abhyasi_id'),
            arrival_date=data.get('arrival_date'),
            departure_date=data.get('departure_date'),
            travel_requirements=TravelRequirements(
                transport_mode=travel_data.get('transport_mode'),
                arrival_location=travel_data.get('arrival_location')
            ),
            accommodation=Accommodation(
                type=accommodation_data.get('type'),
                number_of_people=accommodation_data.get('number_of_people')
            )
        )
        bhandara_entry.save()

        return Response({"message": "Bhandara registration successful"}, status=201)

    except NotUniqueError:
        return Response({"error": "Abhyasi ID already exists. Please use a unique ID."}, status=400)
    except Exception as e:
        return Response({"error": str(e)}, status=400)


@api_view(['GET'])
def get_all_bhandara_records(request):
    try:
        records = Bhandara.objects()
        response_data = []
        for record in records:
            response_data.append({
                "full_name": record.full_name,
                "email":record.email,
                "phone":record.phone,
                "age":record.age,
                "abhyasi_id": record.abhyasi_id,
                "registration_timestamp": record.registration_timestamp,
                "arrival_date": record.arrival_date,
                "departure_date": record.departure_date,
                "travel_requirements": {
                    "transport_mode": record.travel_requirements.transport_mode,
                    "arrival_location": record.travel_requirements.arrival_location
                } if record.travel_requirements else None,
                "accommodation": {
                    "type": record.accommodation.type,
                    "number_of_people": record.accommodation.number_of_people
                } if record.accommodation else None
            })
        return Response(response_data, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=400)



@api_view(['GET'])
def get_bhandara_by_abhyasi_id(request, abhyasi_id):
    try:
        record = Bhandara.objects.get(abhyasi_id=abhyasi_id)
        response_data = {
            "full_name": record.full_name,
            "email": record.email,
            "phone": record.phone,
            "age": record.age,
            "abhyasi_id": record.abhyasi_id,
            "registration_timestamp": record.registration_timestamp,
            "arrival_date": record.arrival_date,
            "departure_date": record.departure_date,
            "travel_requirements": {
                "transport_mode": record.travel_requirements.transport_mode,
                "arrival_location": record.travel_requirements.arrival_location
            } if record.travel_requirements else None,
            "accommodation": {
                "type": record.accommodation.type,
                "number_of_people": record.accommodation.number_of_people
            } if record.accommodation else None
        }
        return Response(response_data, status=200)
    except Bhandara.DoesNotExist:
        return Response({"error": "Abhyasi ID not found"}, status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=400)


@api_view(['POST'])
def register_gitopadesh(request):
    try:
        data = request.data
        accommodation_data = data.get('accommodation', {})

        registration = Gitopadesh(
            full_name=data.get('full_name'),
            abhyasi_id=data.get('abhyasi_id'),
            arrival_date=data.get('arrival_date'),
            language_preference=data.get('language_preference'),
            accommodation=AccommodationDetails(
                type=accommodation_data.get('type'),
                number_of_people=accommodation_data.get('number_of_people')
            ) if accommodation_data else None
        )
        registration.save()
        return Response({"message": "Registration successful"}, status=201)
    except Exception as e:
        return Response({"error": str(e)}, status=400)

@api_view(['GET'])
def get_gitopadesh_by_id(request, abhyasi_id):
    try:
        record = Gitopadesh.objects.get(abhyasi_id=abhyasi_id)
        response_data = {
            "full_name": record.full_name,
            "abhyasi_id": record.abhyasi_id,
            "registration_timestamp": record.registration_timestamp,
            "arrival_date": record.arrival_date,
            "language_preference": record.language_preference,
            "accommodation": {
                "type": record.accommodation.type,
                "number_of_people": record.accommodation.number_of_people
            } if record.accommodation else None
        }
        return Response(response_data, status=200)
    except Gitopadesh.DoesNotExist:
        return Response({"error": "Abhyasi ID not found"}, status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=400)

@api_view(['GET'])
def get_registrations(request):
    event = request.GET.get('event')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')

    query = {}
    if date_from and date_to:
        query['registration_timestamp__gte'] = datetime.strptime(date_from, '%Y-%m-%d')
        query['registration_timestamp__lte'] = datetime.strptime(date_to, '%Y-%m-%d')

    records = Gitopadesh.objects(**query)
    response_data = [
        {
            "full_name": record.full_name,
            "abhyasi_id": record.abhyasi_id,
            "registration_timestamp": record.registration_timestamp,
            "arrival_date": record.arrival_date,
            "language_preference": record.language_preference,
            "accommodation": {
                "type": record.accommodation.type,
                "number_of_people": record.accommodation.number_of_people
            } if record.accommodation else None
        } for record in records
    ]
    return Response(response_data, status=200)

@api_view(['POST'])
def register_hope(request):
    try:
        data = request.data
        accommodation_data = data.get('accommodation', {})

        registration = Hope(
            full_name=data.get('full_name'),
            abhyasi_id=data.get('abhyasi_id'),
            batch_date=data.get('batch_date'),
            experience_level=data.get('experience_level'),
            accommodation=AccommodationDetails(
                type=accommodation_data.get('type')
            ) if accommodation_data else None
        )
        registration.save()
        return Response({"message": "Registration successful"}, status=201)
    except Exception as e:
        return Response({"error": str(e)}, status=400)


@api_view(['GET'])
def get_hope_by_id(request, abhyasi_id):
    try:
        record = Hope.objects.get(abhyasi_id=abhyasi_id)
        response_data = {
            "full_name": record.full_name,
            "abhyasi_id": record.abhyasi_id,
            "registration_timestamp": record.registration_timestamp,
            "batch_date": record.batch_date,
            "experience_level": record.experience_level,
            "accommodation": {
                "type": record.accommodation.type
            } if record.accommodation else None
        }
        return Response(response_data, status=200)
    except Hope.DoesNotExist:
        return Response({"error": "Abhyasi ID not found"}, status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=400)


@api_view(['GET'])
def get_all_hope(request):
    records = Hope.objects()
    response_data = [
        {
            "full_name": record.full_name,
            "abhyasi_id": record.abhyasi_id,
            "registration_timestamp": record.registration_timestamp,
            "batch_date": record.batch_date,
            "experience_level": record.experience_level,
            "accommodation": {
                "type": record.accommodation.type
            } if record.accommodation else None
        } for record in records
    ]
    return Response(response_data, status=200)
