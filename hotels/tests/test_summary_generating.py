from django.test import TestCase
from django.core.management import call_command
from unittest.mock import patch, Mock
from io import StringIO
from hotels.models import GeneratedPropertySummary
from hotels.management.commands.write_summary import Command

class PropertySummaryCommandTests(TestCase):
    def setUp(self):
        self.command = Command()
        self.test_data = {
            'id': '1',
            'title': 'Test Hotel',
            'description': 'Test description',
            'location': 'Test location',
            'price': '100',
            'room_type': 'Single'
        }

    @patch('hotels.management.commands.write_summary.requests.post')
    def test_generate_summary_successful(self, mock_post):
        # Mock successful API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'choices': [{
                'message': {
                    'content': 'This is a generated summary'
                }
            }]
        }
        mock_post.return_value = mock_response

        summary = self.command.Generate_Summary_with_Ollama(
            self.test_data['title'],
            self.test_data['description'],
            self.test_data['location'],
            self.test_data['price'],
            self.test_data['room_type']
        )

        self.assertEqual(summary, 'This is a generated summary')
        
        # Verify API was called with correct parameters
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        self.assertEqual(call_args[1]['headers']['Content-Type'], 'application/json')
        self.assertEqual(call_args[1]['json']['model'], 'tinyllama:latest')
        
        # Verify prompt contains all property information
        prompt = call_args[1]['json']['messages'][0]['content']
        self.assertIn(self.test_data['title'], prompt)
        self.assertIn(self.test_data['description'], prompt)
        self.assertIn(self.test_data['location'], prompt)
        self.assertIn(self.test_data['price'], prompt)
        self.assertIn(self.test_data['room_type'], prompt)


    @patch('hotels.management.commands.write_summary.requests.post')
    def test_generate_summary_api_failure(self, mock_post):
        # Mock failed API response
        mock_response = Mock()
        mock_response.status_code = 500
        mock_post.return_value = mock_response

        summary = self.command.Generate_Summary_with_Ollama(
            self.test_data['title'],
            self.test_data['description'],
            self.test_data['location'],
            self.test_data['price'],
            self.test_data['room_type']
        )

        self.assertEqual(summary, "Error generating summary")

    @patch('builtins.open')
    @patch('csv.DictReader')
    @patch('hotels.management.commands.write_summary.requests.post')
    def test_handle_command(self, mock_post, mock_reader, mock_open):
        # Mock CSV data
        mock_reader.return_value = [self.test_data]
        
        # Mock API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'choices': [{
                'message': {
                    'content': 'Test summary'
                }
            }]
        }
        mock_post.return_value = mock_response

        # Call the command
        out = StringIO()
        call_command('write_summary', stdout=out)

        # Verify database entry was created
        generated_summary = GeneratedPropertySummary.objects.first()
        self.assertIsNotNone(generated_summary)
        self.assertEqual(generated_summary.property_id, 1)
        self.assertEqual(generated_summary.summary, 'Test summary')
        
        # Verify output message
        self.assertIn('Successfully generated summary', out.getvalue())

    @patch('builtins.open')
    @patch('csv.DictReader')
    def test_handle_command_with_multiple_properties(self, mock_reader, mock_open):
        # Mock CSV data with multiple properties
        mock_reader.return_value = [
            {**self.test_data, 'id': '1'},
            {**self.test_data, 'id': '2'},
            {**self.test_data, 'id': '3'}
        ]
        
        with patch('hotels.management.commands.write_summary.requests.post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'choices': [{
                    'message': {
                        'content': 'Test summary'
                    }
                }]
            }
            mock_post.return_value = mock_response

            # Call the command
            call_command('write_summary')

            # Verify multiple database entries were created
            self.assertEqual(GeneratedPropertySummary.objects.count(), 3)
            self.assertEqual(mock_post.call_count, 3)
    

    def test_property_id_conversion(self):
        # Test that property_id is correctly converted to integer
        with patch('builtins.open'), \
             patch('csv.DictReader') as mock_reader, \
             patch('hotels.management.commands.write_summary.requests.post') as mock_post:
            
            mock_reader.return_value = [{**self.test_data, 'id': '123'}]
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'choices': [{
                    'message': {
                        'content': 'Test summary'
                    }
                }]
            }
            mock_post.return_value = mock_response

            call_command('write_summary')
            
            generated_summary = GeneratedPropertySummary.objects.first()
            self.assertEqual(generated_summary.property_id, 123)
            self.assertTrue(isinstance(generated_summary.property_id, int))