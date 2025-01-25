from django.shortcuts import render

# Create your views here.

import random
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Bhandara, TravelRequirements, Accommodation
from mongoengine.errors import NotUniqueError

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



