# LLM Data Generating Project

## Overview
This project leverages a Large Language Model (LLM) to process and generate property data. It is built using Django and focuses on tasks such as rewriting titles and descriptions, generating summaries, ratings, and reviews for properties. Data is initially read from a CSV file and enhanced using the LLM.

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

### 3. Pull Ollama Docker Model
Follow the instructions to pull the required Ollama model:
```bash
docker pull ollama/model-name
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

## Notes
- The `ollama` folder is ignored in the repository to avoid large file uploads. Pull it via Docker as mentioned above.
- Update the project settings if deploying to a production environment.

---

## License
This project is licensed under the MIT License. See the LICENSE file for details.

---

## Contributing
Feel free to open issues or submit pull requests to improve the project!

