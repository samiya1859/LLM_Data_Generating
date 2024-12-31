from django.core.management.base import BaseCommand
import pandas as pd
import requests
import csv
from hotels.models import GeneratedPropertySummary

class Command(BaseCommand):
    help = 'Generate and save summaries for properties'

    def Generate_Summary_with_Ollama(self, title, description, location, price, room_type):
        prompt = f"Generate a summary for the following property: Title: {title}, Description: {description}, Location: {location}, Price: {price}, Room Type: {room_type}"
        url = "http://127.0.0.1:11434/v1/chat/completions"
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "model": "tinyllama:latest",
            "messages": [{"role": "user", "content": prompt}]
        }

        response = requests.post(url, headers=headers, json=data)
        response_data = response.json()

        if response.status_code == 200:

            return response_data['choices'][0]['message']['content']
        else:
            return "Error generating summary"

    def handle(self, *args, **kwargs):
        with open('hotel_datas.csv', 'r') as file:
            reader = csv.DictReader(file)

            for row in reader:
                property_id = int(row['id'])
                title = row['title']
                description = row['description']
                location = row['location']
                price = row['price']
                room_type = row['room_type']

                summary = self.Generate_Summary_with_Ollama(title, description, location, price, room_type)

                GeneratedPropertySummary.objects.create(property_id=property_id,summary=summary)

        self.stdout.write(self.style.SUCCESS('Successfully generated summary and saved to the database'))
