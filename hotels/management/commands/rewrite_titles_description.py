from django.core.management.base import BaseCommand
import pandas as pd
import requests
import csv
from hotels.models import GeneratedHotelTD

class Command(BaseCommand):
    help = 'Rewrite property titles and descriptions using the Ollama model'

    def rewrite_with_ollama(self, original_title, original_description):
        
        prompt = f"Rewrite the following: Title: {original_title}, Description: {original_description}"
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
            
            rewritten_content = response_data['choices'][0]['message']['content']
            
            try:
                title_part, description_part = rewritten_content.split("Description:", 1)
                return title_part.strip(), description_part.strip()
            except ValueError:
                title_part = rewritten_content.split(".")[0]  
                description_part = rewritten_content[len(title_part):].strip() 
                return title_part.strip(), description_part.strip()
        else:
            return original_title, original_description
  
    def handle(self, *args, **kwargs):
        with open('hotel_datas.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                original_title = row['title']
                original_description = row['description']
                rewritten_title, rewritten_description = self.rewrite_with_ollama(original_title, original_description)
    
                
                rewritten_title = rewritten_title[:150]
                GeneratedHotelTD.objects.create(
                    title=rewritten_title,
                    description=rewritten_description
                )
    
        self.stdout.write(self.style.SUCCESS('Successfully processed hotel data and saved to the database'))
    