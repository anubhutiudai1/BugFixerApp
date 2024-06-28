from flask import Flask, request, jsonify, render_template
import os
import logging
from datetime import datetime, timezone, timedelta
from google.oauth2 import service_account
from google.cloud import aiplatform
from vertexai.preview.generative_models import GenerativeModel

app = Flask(__name__, static_folder='static')

# Set up Gemini API credentials
# credentials = service_account.Credentials.from_service_account_file(
#     'C:\Bug fixer app\credentials.json'
# )
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "C:/BugFixerApp/credentials.json"

# Configure logging
log_format = '%(asctime)s %(levelname)s: %(message)s'
logging.basicConfig(filename='app.log', level=logging.DEBUG, format=log_format)

# Function to convert UTC to IST
def utc_to_ist(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=timezone(timedelta(hours=5, minutes=30)))

@app.route('/')
def index():
    
    return render_template('index.html')

@app.route('/fix_code', methods=['POST'])
def fix_code():
    data = request.get_json()
    input_code = data['code']

    
    fixed_code = fix_code_with_gemini(input_code)

    return fixed_code

def fix_code_with_gemini(code):
    try:
        aiplatform.init(project="lively-nimbus-427218-d4", location="us-central1")
        google_model = GenerativeModel("gemini-1.5-pro-001")
        prompt= f"""```tool_code
{code}
Find and fix the errors in the above code. don't explain the error just respond with fixed code```"""
        responses = google_model.generate_content(
                    prompt,
                    stream=True)

        response_texts = [response.text for response in responses]

        fixed_code=''.join(response_texts)
        if '```tool_code' in fixed_code:
            fixed_code = fixed_code.split('```tool_code')[1].split('```')[0].strip()

        
        return fixed_code

    except Exception as e:
        app.logger.error(f'Error fixing code: {str(e)}')
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)