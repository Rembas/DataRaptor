import psycopg2
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from sklearn.ensemble import RandomForestClassifier
import tensorflow as tf
import numpy as np
import time

# Function to predict missing form fields using AI (based on page structure)
def predict_element(driver, html, label):
    soup = BeautifulSoup(html, 'html.parser')
    potential_elements = soup.find_all("input")  # Example: Look for input elements

    # Try to match the label to the 'name' or 'id' of the input fields
    for element in potential_elements:
        if label.lower() in element.get('name', '').lower() or label.lower() in element.get('id', '').lower():
            return driver.find_element(By.NAME, element.get('name'))

    # If no element is found, raise an error
    raise Exception(f"Element with label {label} not found")

# Function to dynamically adapt the scraper based on changes in the page structure
def dynamic_scrape(driver, html):
    soup = BeautifulSoup(html, 'html.parser')
    elements = soup.find_all("div")  # Example: Analyze all <div> elements

    # Using a pre-trained Random Forest model to detect structure changes
    clf = RandomForestClassifier()

    # Example dummy training data (replace with real data)
    X_train = np.array([[0, 1], [1, 0], [0, 0], [1, 1]])
    y_train = np.array([0, 1, 0, 1])  # 0 = No significant change, 1 = Significant change

    clf.fit(X_train, y_train)

    # Extracting features from the current DOM
    X_test = np.array([len(elements), 1])  # Example: Number of elements
    change_prediction = clf.predict([X_test])

    if change_prediction == 1:
        print("Change detected, updating scraping rules.")
        return True
    else:
        print("No significant change detected.")
        return False

# Function to perform login using Selenium, with AI prediction for missing fields
def perform_login(url, username, password):
    options = webdriver.ChromeOptions()
    options.headless = True  # Use headless mode for production

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(url)
        time.sleep(2)  # Wait for the page to load

        html = driver.page_source

        # Predict the username field
        try:
            username_input = driver.find_element(By.ID, 'username')
        except:
            username_input = predict_element(driver, html, 'username')

        username_input.send_keys(username)

        # Predict the password field
        try:
            password_input = driver.find_element(By.ID, 'password')
        except:
            password_input = predict_element(driver, html, 'password')

        password_input.send_keys(password)

        # Predict and click the submit button
        try:
            submit_button = driver.find_element(By.ID, 'submit')
        except:
            submit_button = predict_element(driver, html, 'submit')

        submit_button.click()

        # Wait and check if login was successful
        time.sleep(5)
        if "login failed" in driver.page_source.lower():
            return {"status": "failed", "message": "Login failed. Check credentials or site status."}
        else:
            return {"status": "success", "message": "Login successful!"}

    except Exception as e:
        return {"status": "error", "message": str(e)}

    finally:
        driver.quit()

# Function to classify data using a Random Forest model
def classify_data(data):
    # Example dataset: [price, description_length]
    X = np.array([[20, 100], [30, 200], [25, 150], [35, 120]])
    y = np.array([0, 1, 0, 1])  # 0 = Category A, 1 = Category B

    # Split dataset and train classifier
    classifier = RandomForestClassifier()
    classifier.fit(X, y)

    # Classify the new data extracted
    new_data = np.array([data['price'], len(data['description'])])
    predicted_category = classifier.predict([new_data])

    return predicted_category[0]  # Return the predicted category

# Function to predict price variations using a TensorFlow model
def predict_price(data):
    # Define a neural network model
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(64, activation='relu', input_shape=(2,)),  # Example with two features
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(1)  # Predicting a single value (price)
    ])

    model.compile(optimizer='adam', loss='mse')

    # Example training data (replace with real data)
    X_train = np.array([[20, 100], [30, 200], [25, 150], [35, 120]])
    y_train = np.array([22, 32, 27, 37])

    model.fit(X_train, y_train, epochs=10)

    # Predict price for new extracted data
    new_data = np.array([data['price'], len(data['description'])])
    predicted_price = model.predict([new_data])

    return predicted_price[0][0]  # Return the predicted price

# Function to save data into PostgreSQL
def save_to_postgres(products):
    try:
        # Connect to PostgreSQL database
        connection = psycopg2.connect(
            host="localhost",  # Adjust to your setup
            database="your_database",
            user="your_user",
            password="your_password"
        )
        cursor = connection.cursor()

        # Create table if not exists
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                name TEXT,
                price TEXT,
                description TEXT
            );
        ''')

        # Insert products into the table
        for product in products:
            cursor.execute('''
                INSERT INTO products (name, price, description) VALUES (%s, %s, %s)
            ''', product)

        # Commit and close connection
        connection.commit()
        cursor.close()
        connection.close()
        print("Data successfully saved to PostgreSQL.")

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")

# Function to perform login, scrape data, and save to PostgreSQL
def perform_scraping_and_save(url, username, password):
    options = webdriver.ChromeOptions()
    options.headless = True  # Headless mode

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(url)
        time.sleep(2)  # Allow the page to load

        # Perform login logic (if necessary)
        result = perform_login(url, username, password)
        if result['status'] != 'success':
            return result  # If login failed, return the error

        # Once logged in, scrape product details (example structure)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        products = []
        for product_div in soup.find_all('div', class_='product'):  # Update selector as necessary
            product_name = product_div.find('h2').text.strip()
            price = product_div.find('span', class_='price').text.strip()
            description = product_div.find('p', class_='description').text.strip()
            products.append((product_name, price, description))

        # Save the scraped data to PostgreSQL
        save_to_postgres(products)

        return {"status": "success", "message": "Data scraped and saved to PostgreSQL"}

    except Exception as e:
        return {"status": "error", "message": str(e)}

    finally:
        driver.quit()