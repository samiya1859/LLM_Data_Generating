from django.test import TestCase
from decimal import Decimal
from hotels.models import GeneratedHotelTD, GeneratedPropertySummary, GeneratePropertyRatingReview

class GeneratedHotelTDTests(TestCase):
    def setUp(self):
        """Set up test data for GeneratedHotelTD"""
        self.hotel = GeneratedHotelTD.objects.create(
            title="Test Hotel",
            description="This is a test hotel description"
        )

    def test_hotel_creation(self):
        """Test if hotel is created correctly"""
        self.assertEqual(self.hotel.title, "Test Hotel")
        self.assertEqual(self.hotel.description, "This is a test hotel description")

    def test_hotel_str_method(self):
        """Test the string representation of GeneratedHotelTD"""
        self.assertEqual(str(self.hotel), "Test Hotel")

    def test_title_max_length(self):
        """Test if title max length is enforced"""
        max_length = self.hotel._meta.get_field('title').max_length
        self.assertEqual(max_length, 255)

class GeneratedPropertySummaryTests(TestCase):
    def setUp(self):
        """Set up test data for GeneratedPropertySummary"""
        self.property_summary = GeneratedPropertySummary.objects.create(
            property_id=12345,
            summary="This is a test property summary"
        )

    def test_property_summary_creation(self):
        """Test if property summary is created correctly"""
        self.assertEqual(self.property_summary.property_id, 12345)
        self.assertEqual(self.property_summary.summary, "This is a test property summary")

    def test_property_summary_str_method(self):
        """Test the string representation of GeneratedPropertySummary"""
        expected_str = "Summary for propertyID 12345"
        self.assertEqual(str(self.property_summary), expected_str)

    def test_property_id_integer_field(self):
        """Test if property_id accepts and stores integer values"""
        new_summary = GeneratedPropertySummary.objects.create(
            property_id=54321,
            summary="Another test summary"
        )
        self.assertEqual(new_summary.property_id, 54321)
        self.assertTrue(isinstance(new_summary.property_id, int))

class GeneratePropertyRatingReviewTests(TestCase):
    def setUp(self):
        """Set up test data for GeneratePropertyRatingReview"""
        self.property_review = GeneratePropertyRatingReview.objects.create(
            property_id=12345,
            rating=Decimal('4.5'),
            review="This is a test review"
        )

    def test_property_review_creation(self):
        """Test if property review is created correctly"""
        self.assertEqual(self.property_review.property_id, 12345)
        self.assertEqual(self.property_review.rating, Decimal('4.5'))
        self.assertEqual(self.property_review.review, "This is a test review")

    def test_property_review_str_method(self):
        """Test the string representation of GeneratePropertyRatingReview"""
        expected_str = "Review for Property 12345 - Rating: 4.5"
        self.assertEqual(str(self.property_review), expected_str)

    def test_rating_decimal_constraints(self):
        """Test if rating field respects decimal constraints"""
        self.property_review.rating = Decimal('3.7')
        self.property_review.save()
        self.assertEqual(self.property_review.rating, Decimal('3.7'))

    def test_rating_max_digits_and_decimal_places(self):
        """Test the max_digits and decimal_places constraints of rating field"""
        rating_field = self.property_review._meta.get_field('rating')
        self.assertEqual(rating_field.max_digits, 3)
        self.assertEqual(rating_field.decimal_places, 1)

    def test_invalid_rating_value(self):
        """Test that invalid rating values raise an exception"""
        with self.assertRaises(Exception):
            GeneratePropertyRatingReview.objects.create(
                property_id=12345,
                rating=Decimal('100.5'), 
                review="This should fail"
            )