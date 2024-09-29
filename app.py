from flask import Flask, render_template, request, jsonify
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
from ai_agent import perform_login, classify_data, predict_price, perform_scraping_and_save  # Import AI and scraping functions

app = Flask(__name__)

# Route to render the index.html form
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle form submission and perform login/scraping
@app.route('/submit-url', methods=['POST'])
def submit_url():
    # Retrieve form data
    url = request.form.get('url')
    username = request.form.get('username')
    password = request.form.get('password')

    # Ensure the URL is provided
    if not url:
        return jsonify({"error": "URL is required"}), 400

    # Set up Firefox driver in headless mode
    options = Options()
    options.headless = True
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)

    try:
        # Perform login using the AI-enhanced web scraper
        result = perform_login(url, username, password)

        if result['status'] == 'success':
            # Example of classified data (replace with real scraped data)
            extracted_data = {'price': 30, 'description': 'Sample product description'}

            # Classify the extracted data
            category = classify_data(extracted_data)

            # Predict price variation using a neural network
            predicted_price = predict_price(extracted_data)

            # Perform scraping and save to PostgreSQL
            scraping_result = perform_scraping_and_save(url, username, password)
            if scraping_result['status'] != 'success':
                return jsonify({"error": scraping_result['message']}), 500

            # Return a successful response with classification, prediction, and scraping result
            return jsonify({
                "message": "Login, scraping, and data classification successful!",
                "category": category,
                "predicted_price": predicted_price,
                "scraping_message": scraping_result['message']
            })
        else:
            # Return an error message if login failed
            return jsonify({"error": result['message']}), 500

    except Exception as e:
        # Handle exceptions and return error message
        return jsonify({"error": str(e)}), 500
    finally:
        # Quit the driver regardless of success or failure
        driver.quit()

# Main entry point for Flask application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
