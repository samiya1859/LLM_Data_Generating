# LLM Data Generating Project

## Overview
This project leverages a Large Language Model (LLM) to process and generate property data. It is built using Django and focuses on tasks such as rewriting titles and descriptions, generating summaries, ratings, and reviews for properties. Data is initially read from a CSV file and enhanced using the LLM. Later storing datas into PostgreSQl Database. 

---

## Features

- **Rewriting Titles and Descriptions**: Enhances property details using an Ollama model.
- **Generating Property Summaries**: Summarizes property information in a concise format.
- **Creating Ratings and Reviews**: Generates synthetic ratings and reviews for properties.


---

## Folder Structure
```plaintext
.
├── data_rewrite/           # Main app with settings and configurations
├── hotels/                # App for handling property data models and commands
├── ollama/                # Docker-pulled folder (ignored in repo)
├── hotel_datas.csv        # Input CSV with property data
├── manage.py              # Django project manager
└── README.md              # Project documentation
```

---

## Prerequisites
- Python 3.9+
- Docker
- Django 4.0+
- Ollama LLM Model (pulled via Docker)

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/samiya1859/LLM_Data_Generating.git
cd LLM_Data_Generating
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. pull Ollama and Postgres
**before pulling you have to set the docker-compose.yml file as per your database,version information.**
```bash
docker-compose up -d
```
The -d flag will run the services in the background.

**Check the Logs**
```bash
docker-compose logs -f ollama
```
This will show the logs for the ollama service in real-time

**Stop the Services**
When you're done, stop and remove the containers by running:
```bash
docker-compose down
```

### 4. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Populate the Database
Load initial property data from the CSV file:
```bash
python manage.py rewrite_titles_description
python manage.py generate_summaries
python manage.py generate_ratings_reviews
```

---

## Usage

### Rewriting Titles and Descriptions
Run the custom management command:
```bash
python manage.py rewrite_titles_description
```

### Generating Summaries
Run the summary generator:
```bash
python manage.py generate_summaries
```

### Generating Ratings and Reviews
Run the rating and review generator:
```bash
python manage.py generate_ratings_reviews
```

---

## CSV File Structure
Ensure your `hotel_datas.csv` file follows this structure:
| id | title | rating | location | latitude | longitude | room_type | price | description |
|----|-------|--------|----------|----------|-----------|-----------|-------|-------------|

---
### Testing the LLM Model
This section outlines how to test the functionality of the Ollama model integration, ensuring that the rewritten titles, descriptions, summaries, and generated ratings are accurate and properly populated in your Django models.

```bash
python manage.py test

```
### Getting Code Coverage
To ensure that your tests cover a substantial portion of the code, you can use a code coverage tool. This section explains how to set up and use coverage to measure the effectiveness of your tests.
#### Install Coverage Package
First, you need to install the coverage package, which is used to measure the code coverage of your tests. You can install it by running:
```bash
pip install coverage
```
#### Running Tests with Coverage
Once coverage is installed, you can run your tests with coverage tracking by using the following command:
```bash
coverage run --source='.' manage.py test
```
- --source='.' specifies the directory (your entire project) to monitor for coverage. This tells coverage to track which lines of your code are executed while the tests run.
- manage.py test runs your Django tests.
  ####    Generate Coverage Report
After running the tests with coverage, generate a human-readable report:
```bash
coverage report
```
This will display a summary of the code coverage directly in your terminal. It will show you which lines of your code were executed and which were missed.

If you want a more detailed, line-by-line report, you can run:
```bash
coverage html
```
This will generate an htmlcov directory with an HTML report. You can open the index.html file in your browser to view the coverage results.
```bash
open htmlcov/index.html  # For macOS or Linux
```

## Notes
- The `ollama` folder is ignored in the repository to avoid large file uploads. Pull it via Docker as mentioned above.
- Update the project settings if deploying to a production environment.

---

## License
This project is licensed under the MIT License. See the LICENSE file for details.

---

## Contributing
Feel free to open issues or submit pull requests to improve the project!

