from django.core.management.base import BaseCommand
import requests
import csv
import re
import json
from hotels.models import GeneratePropertyRatingReview


class Command(BaseCommand):
    help = 'Generate and save ratings and reviews for properties'

    def generate_rating_review_with_ollama(self, title, description, location, room_type, price):
        rating_prompt = f"Assign a rating out of 5 stars (use one decimal place) for this property based on the following details:\n" \
                        f"Title: {title},\n" \
                        f"Description: {description},\n" \
                        f"Location: {location},\n" \
                        f"Room Type: {room_type},\n" \
                        f"Price: {price}\n" \
                        f"Please provide the rating in decimal format."

        review_prompt = f"Generate a detailed review for the following property:\n" \
                        f"Title: {title},\n" \
                        f"Description: {description},\n" \
                        f"Location: {location},\n" \
                        f"Room Type: {room_type},\n" \
                        f"Price: {price}\n" \
                        f"Please provide a comprehensive review describing the property's features, amenities, and overall experience."

        url = "http://127.0.0.1:11434/v1/chat/completions"
        headers = {"Content-Type": "application/json"}

        # Request for rating
        data_rating = {"model": "tinyllama:latest", "messages": [{"role": "user", "content": rating_prompt}]}
        response_rating = requests.post(url, headers=headers, json=data_rating)

        if response_rating.status_code == 200:
            try:
                response_data_rating = response_rating.json()
                content_rating = response_data_rating['choices'][0]['message']['content']
                print(f"Rating Content: {content_rating}")

                # Match decimal rating
                rating_match = re.search(r'Rating:\s*(\d+\.\d+)', content_rating)
                if rating_match:
                    rating = float(rating_match.group(1))
                else:
                    print(f"Rating extraction failed for property {title}, defaulting to 4.5.")
                    rating = 4.5
            except (IndexError, ValueError, KeyError) as e:
                print(f"Error processing rating response: {e}")
                rating = 4.5
        else:
            print(f"Error generating rating: {response_rating.status_code} - {response_rating.text}")
            rating = 4.5

        # Request for review
        data_review = {"model": "tinyllama:latest", "messages": [{"role": "user", "content": review_prompt}]}
        response_review = requests.post(url, headers=headers, json=data_review)

        if response_review.status_code == 200:
            try:
                response_data_review = response_review.json()
                content_review = response_data_review['choices'][0]['message']['content']
                print(f"Review Content: {content_review}")

                
                review = re.sub(r'Rating.*?stars?', '', content_review, flags=re.IGNORECASE).strip()
            except (IndexError, ValueError, KeyError) as e:
                print(f"Error processing review response: {e}")
                review = "Default review: This is a great property!"
        else:
            print(f"Error generating review: {response_review.status_code} - {response_review.text}")
            review = "Default review: This is a great property!"

        return rating, review



    def handle(self, *args, **kwargs):
        processed_properties = set()  

        with open('hotel_datas.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                property_id = row['id']
                if property_id in processed_properties:
                    continue  
                processed_properties.add(property_id)
    
                title = row['title']
                description = row['description']
                location = row['location']
                room_type = row['room_type']
                price = row['price']
    
                # Generate rating and review
                generated_rating, generated_review = self.generate_rating_review_with_ollama(
                    title, description, location, room_type, price
                )
    
                # Save to the database
                GeneratePropertyRatingReview.objects.create(
                    property_id=property_id,
                    rating=generated_rating,
                    review=generated_review
                )
    
                # Print for debugging
                self.stdout.write(
                    self.style.SUCCESS(f"Review for Property {property_id} - Rating: {generated_rating}")
                )

        self.stdout.write(
            self.style.SUCCESS('Successfully generated ratings and reviews for properties.')
        )

