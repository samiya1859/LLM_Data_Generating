
from django.db import models

class GeneratedHotelTD(models.Model):
    title = models.CharField(max_length=255)  
    description = models.TextField() 
    def __str__(self):
        return self.title


class GeneratedPropertySummary(models.Model):
    property_id = models.IntegerField()  
    summary = models.TextField()

    def __str__(self):
        return f"Summary for propertyID {self.property_id}"


class GeneratePropertyRatingReview(models.Model):
    property_id = models.IntegerField()  
    rating = models.DecimalField(max_digits=3, decimal_places=1) 
    review = models.TextField() 

    def __str__(self):
        return f"Review for Property {self.property_id} - Rating: {self.rating}"