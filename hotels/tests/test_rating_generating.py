from unittest.mock import patch, Mock, MagicMock
from django.core.management import call_command
from io import StringIO
from django.test import TestCase
from decimal import Decimal
from hotels.models import GeneratePropertyRatingReview

class CommandTest(TestCase):
    @patch('requests.post')
    def test_generate_rating_and_review(self, mock_post):
        def side_effect(*args, **kwargs):
            if args[0].endswith('rating-endpoint'):  # Adjust URL matching logic as needed
                return Mock(status_code=200, json=lambda: {'choices': [{'message': {'content': 'Rating: 4.5 stars'}}]})
            elif args[0].endswith('review-endpoint'):  # Adjust URL matching logic as needed
                return Mock(status_code=200, json=lambda: {'choices': [{'message': {'content': 'Great property, highly recommend it!'}}]})
            else:
                raise ValueError('Unexpected request')
    
            # Set the side_effect function
            mock_post.side_effect = side_effect
        
            # Call the management command
            out = StringIO()
            call_command('generate_rating_review', stdout=out)
        
            # Check for expected output
            self.assertIn('Rating:', out.getvalue())
            self.assertIn('Review:', out.getvalue())



    def capture_stdout(self, func):
        """
        Captures the standard output during the execution of a function
        """
        import io
        from contextlib import redirect_stdout
        
        out = io.StringIO()
        with redirect_stdout(out):
            func()
        return out.getvalue()


    @patch('hotels.management.commands.generate_rating_review.requests.post')
    def test_api_failure_handling(self, mock_post):
        """
        Test that the command handles API failures gracefully
        """

        
        # Simulate an API failure by having the mock return a non-200 status code
        mock_post.return_value.status_code = 500  # Simulating server error
        mock_post.return_value.text = "Internal Server Error"
        
        # Call the command
        out = self.capture_stdout(lambda: call_command('generate_rating_review'))

        # Check that the error message is in the output
        self.assertIn("Error generating rating:", out)
        self.assertIn("Error generating review:", out)
        
        # Ensure default values are used (rating = 4.5, default review)
        # Check if default review was used
        review = GeneratePropertyRatingReview.objects.first().review
        rating = GeneratePropertyRatingReview.objects.first().rating
        
        self.assertEqual(review, "Default review: This is a great property!")
        self.assertEqual(rating, 4.5) 

    @patch('builtins.open')
    @patch('requests.post')
    def test_duplicate_property_handling(self, mock_post, mock_open):
        """Test handling of duplicate property IDs"""
        
        # Mock CSV file with duplicate entries
        mock_open.return_value.__enter__.return_value = StringIO(
            "id,title,description,location,room_type,price\n"
            "1,Test Hotel,Nice hotel,Downtown,Suite,200\n"
            "1,Test Hotel,Nice hotel,Downtown,Suite,200\n"
        )
        
        # Setup mock responses for rating and review
        self.mock_rating_response = {
            "rating": 4.5,
            "review": "Great property, highly recommend it!"
        }
        
        self.mock_review_response = {
            "rating": 4.5,
            "review": "Great property, highly recommend it!"
        }

        # Mock the post requests for rating and review
        mock_post.return_value = MagicMock(status_code=200, json=lambda: self.mock_rating_response)

        # Call the command
        out = StringIO()
        call_command('generate_rating_review', stdout=out)

        # Verify only one entry was created for the duplicate property_id
        review_count = GeneratePropertyRatingReview.objects.filter(property_id=1).count()
        self.assertEqual(review_count, 1)

        # Optionally, you can print the command output if needed for debugging
        print(out.getvalue())


   
    @patch('builtins.open')
    @patch('requests.post')
    def test_rating_extraction_failure(self, mock_post, mock_open):
        """Test handling of invalid rating format in API response"""
        
        # Setup mock response with invalid rating format (non-numeric)
        mock_invalid_rating_response = {
            "choices": [{
                "message": {
                    "content": "The rating is excellent"  # Invalid non-numeric rating
                }
            }]
        }

        # Setup mock response for review (fallback response)
        self.mock_review_response = {
            "rating": 4.5,
            "review": "Great property, highly recommend it!"
        }

        # Mock post request to return invalid rating response
        mock_post.return_value = MagicMock(
            status_code=200,
            json=lambda: mock_invalid_rating_response  # Always returns invalid response
        )
        
        # Mock CSV file with property data
        mock_open.return_value.__enter__.return_value = StringIO(
            "id,title,description,location,room_type,price\n"
            "1,Test Hotel,Nice hotel,Downtown,Suite,200\n"
        )
        
        # Call the command
        out = StringIO()
        call_command('generate_rating_review', stdout=out)
        
        # Verify that a default rating was used when invalid rating is extracted
        review = GeneratePropertyRatingReview.objects.get(property_id=1)
        
        # Verify that the default rating was set (e.g., 4.5)
        self.assertEqual(review.rating, Decimal('4.5'))

        # Optionally, print the output for debugging
        print(out.getvalue())      