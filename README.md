# DataRaptor

DataRaptor is an intelligent web scraping tool designed to automate interactions with websites that lack APIs. It logs into websites, scrapes data, classifies it, predicts trends like price variations, and stores the extracted information into a PostgreSQL database.

## Features
- **Login Automation**: AI-enhanced login automation using Selenium and machine learning to predict missing form fields.
- **Dynamic Scraping**: Adapts to website changes using machine learning to dynamically update scraping logic.
- **Data Classification**: Classifies scraped data into categories (e.g., product categories) using scikit-learn.
- **Price Prediction**: Uses a neural network (TensorFlow) to predict price variations based on historical data.
- **Database Integration**: Stores scraped data in a PostgreSQL database for future analysis.

## Requirements

- **Python 3.x**
- **PostgreSQL**
- Python libraries:
  - `selenium`
  - `beautifulsoup4`
  - `psycopg2-binary`
  - `tensorflow`
  - `scikit-learn`
  - `webdriver-manager`
- Browser drivers:
  - **Firefox**: `geckodriver`
  - **Chrome**: `chromedriver`
- **Docker** (optional but recommended for deployment)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/dataraptor.git
   cd dataraptor

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt

3. Set up PostgreSQL:
   - Install PostgreSQL and create a database:
     ```sql
     CREATE DATABASE your_database;
     CREATE USER your_user WITH PASSWORD 'your_password';
     GRANT ALL PRIVILEGES ON DATABASE your_database TO your_user;

4. Update `ai_agent.py` to configure your PostgreSQL connection:
   ```sql
   connection = psycopg2.connect(
      host="localhost",
      database="your_database",
      user="your_user",
      password="your_password"
   )

## Configuration
Ensure the following configurations are set up correctly:

1. Browser Drivers: Install geckodriver for Firefox or chromedriver for Chrome. You can manage drivers automatically using webdriver-manager.

2. PostgreSQL: Ensure PostgreSQL is installed and running. Update the credentials in ai_agent.py to connect to your database.

3. Environment Variables (optional): Set environment variables for sensitive information like database credentials or API keys.

## Running the Application
1. Start the Flask server:
   ```bash
   python app.py

2. Open your browser and navigate to:
   ```site
   http://localhost:5000

3. Enter the URL of the website you want to scrape, along with the username and password if required, and click submit.

## Docker Setup (Optional)
If you prefer using Docker, follow these steps to run the application:

1. Install Docker and Docker Compose.

2. Create a `docker-compose.yml` file (if not already included)
   ```yaml
   version: '3'
   services:
     app:
       build: .
       ports:
          - "5000:5000"
     db:
       image: postgres
       environment:
         POSTGRES_USER: your_user
         POSTGRES_PASSWORD: your_password
         POSTGRES_DB: your_database
       ports:
          - "5432:5432"

3. Build and start the containers:
   ```bash
   docker-compose up --build

## Usage
1. **Login:** The application will automatically log into the target website using the provided credentials.
2. **Scraping:** After login, the app will scrape data such as product names, prices, and descriptions from the website.
3. **Classification and Prediction:** The app will classify the scraped data into predefined categories and predict price variations using machine learning.
4. **Data Storage:** All scraped data will be stored in the PostgreSQL database.

## Testing
To test the application, follow these steps:

1. Ensure PostgreSQL is running and properly configured.
2. Use the Flask form to input test URLs and credentials to verify the login, scraping, and classification functionalities.
3. Check the PostgreSQL database to ensure the data is correctly stored.

## Known Issues
- Ensure the website you are scraping does not use CAPTCHAs, as the current implementation may not handle them well.
- Make sure the correct browser drivers (`geckodriver` or `chromedriver`) are installed and properly configured.
. If using Docker, ensure that the web drivers and PostgreSQL service are properly configured inside the container.

## Contributing
We welcome contributions! Please create a pull request or open an issue if you'd like to contribute to the project. Ensure that all changes are properly tested before submitting.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
