from flask import Flask, request, jsonify, render_template
import os
import requests
from google.oauth2 import service_account
from google.cloud import aiplatform
from vertexai.preview.generative_models import GenerativeModel

app = Flask(__name__, static_folder='static')

# Set up Gemini API credentials
# credentials = service_account.Credentials.from_service_account_file(
#     'C:\Bug fixer app\credentials.json'
# )
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "C:/BugFixerApp/credentials.json"

# Gemini API endpoint
#gemini_api_url = 'https://generativelanguage.googleapis.com/v1beta2/models/text-bison-001:generateText'

@app.route('/')
def index():

    return render_template('index.html')

@app.route('/fix_code', methods=['POST'])
def fix_code():
    data = request.get_json()
    input_code = data['code']

    fixed_code = fix_code_with_gemini(input_code)

    return fixed_code #jsonify({'fixed_code': fixed_code})

def fix_code_with_gemini(code):
    aiplatform.init(project="lively-nimbus-427218-d4", location="us-central1")
    google_model = GenerativeModel("gemini-1.5-pro-001")
    prompt= f"""```tool_code
{code}
Find and fix the errors in the above code. don't explain the error just respond with fixed code```"""
    responses = google_model.generate_content(
                prompt,
                stream=True)

    response_texts = [response.text for response in responses]
    # headers = {
    #     'Authorization': f'Bearer {credentials.token}',
    #     'Content-Type': 'application/json'
    # }
#     data = {
#         "prompt": {
#             "text": f"""```tool_code
# {code}
# Find and fix the errors in the above code.```"""
#         },
#         "temperature": 0.2, 
#         "top_k": 40, 
#         "top_p": 0.95,
#         "candidate_count": 1 
#     }

    # response = requests.post(gemini_api_url, headers=headers, json=data)
    # response.raise_for_status()  # Raise an exception for bad status codes

    # fixed_code = response.json()['candidates'][0]['output']
    
    fixed_code=''.join(response_texts)
    if '```tool_code' in fixed_code:
        fixed_code = fixed_code.split('```tool_code')[1].split('```')[0].strip()
    
    return fixed_code


if __name__ == '__main__':
    app.run(debug=True)