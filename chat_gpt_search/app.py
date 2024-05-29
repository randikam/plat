from flask import Flask, render_template, request
from openai import OpenAI
from datetime import datetime

app = Flask(__name__)
client = OpenAI(api_key="add_open_api_key_here")

# Save file with date and timestamp
current_datetime = datetime.now().strftime("%d-%m-%Y %H-%M-%S")

# Define the function to generate test cases
def generate_test_cases(requirement):
    prompt = "You are a helpful assistant capable of generating software test cases from the requirements. Test cases should have Test Case ID, Test Case Name, Description, Steps, Expected results and an indication if they are regression candidate. Please assign priority and complexity High, Medium or Low to the test cases and provide a justification for the both priority and complexity"
    response = client.chat.completions.create(
        model="gpt-4-0125-preview",  # Specify the engine appropriate for your use case
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": requirement}
        ],
    )
    return response.choices[0].message.content.strip()

@app.route('/', methods=['GET', 'POST'])
def index():
    error_message = None
    test_cases = None

    if request.method == 'POST':
        requirement = request.form.get('requirement')
        if requirement:
            try:
                test_cases = generate_test_cases(requirement)
            except Exception as e:
                error_message = 'An error occurred while generating test cases: ' + str(e)
        else:
            error_message = 'Please enter a requirement to generate test cases.'

    return render_template('index.html', error=error_message, test_cases=test_cases)

if __name__ == '__main__':
    app.run(debug=True)
