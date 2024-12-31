import csv
from io import StringIO
import os
from django.test import TestCase
from unittest.mock import patch

class CSVReadingTest(TestCase):

    @patch("builtins.open")
    def test_csv_parsing(self, mock_open):
        # Path to the CSV file
        file_path = os.path.join(os.path.dirname(__file__), 'test_csv.csv')
        print(file_path)

        # Data you want the mock to return, no leading spaces
        mock_file_data = """id,title,rating,location,latitude,longitude,room_type,price,description
1,Hotel Sunshine,4.5,Los Angeles,34.0522,-118.2437,Private Room,150,Cozy private room with a beautiful view of the city skyline.
2,Ocean Breeze Hotel,4.7,Miami,25.7617,-80.1918,Entire House,220,Beachfront property with modern amenities and spacious rooms.
3,Mountain Retreat,4.8,Denver,39.7392,-104.9903,Shared Room,80,A peaceful retreat in the mountains. perfect for nature lovers."""

        # Set the mock to return the file data
        mock_open.return_value = StringIO(mock_file_data.strip())

        # Now open the file using the mock
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)

            # Read the first row
            row1 = next(reader)
            self.assertEqual(row1['id'].strip(), '1')  # Strip any extra spaces
            self.assertEqual(row1['title'].strip(), 'Hotel Sunshine')  # Strip if necessary
            self.assertEqual(row1['rating'].strip(), '4.5')
            self.assertEqual(row1['location'].strip(), 'Los Angeles')
            self.assertEqual(row1['room_type'].strip(), 'Private Room')
            self.assertEqual(row1['price'].strip(), '150')
            self.assertEqual(row1['description'].strip(), 'Cozy private room with a beautiful view of the city skyline.')

            # Read the second row
            row2 = next(reader)
            self.assertEqual(row2['id'].strip(), '2')
            self.assertEqual(row2['title'].strip(), 'Ocean Breeze Hotel')
            self.assertEqual(row2['rating'].strip(), '4.7')
            self.assertEqual(row2['location'].strip(), 'Miami')
            self.assertEqual(row2['room_type'].strip(), 'Entire House')
            self.assertEqual(row2['price'].strip(), '220')
            self.assertEqual(row2['description'].strip(), 'Beachfront property with modern amenities and spacious rooms.')

            # Read the third row
            row3 = next(reader)
            self.assertEqual(row3['id'].strip(), '3')
            self.assertEqual(row3['title'].strip(), 'Mountain Retreat')
            self.assertEqual(row3['rating'].strip(), '4.8')
            self.assertEqual(row3['location'].strip(), 'Denver')
            self.assertEqual(row3['room_type'].strip(), 'Shared Room')
            self.assertEqual(row3['price'].strip(), '80')
            self.assertEqual(row3['description'].strip(), 'A peaceful retreat in the mountains. perfect for nature lovers.')
