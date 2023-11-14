import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
import requests
import shutil
import secrets

app = Flask(__name__)

# Generate a secure random key with 24 bytes for the secret key
secret_key = secrets.token_hex(24)
# Set the secret key for session management
app.secret_key = secret_key 
deepai_api_key = 'b02dbf77-82c0-4e62-98c3-47f6c441b3c4'

def generate_logo(text, style, new_text=None, new_style=None):
    endpoint = 'https://api.deepai.org/api/text2img'
    
    headers = {
        'api-key': deepai_api_key,
    }

    data = {
        'text': text if not new_text else new_text,  # Use new_text if provided, otherwise use the original text
        'style': style if not new_style else new_style,  # Use new_style if provided, otherwise use the original style
    }

    response = requests.post(endpoint, headers=headers, data=data)
    
    if response.status_code == 200:
        result = response.json()
        return result.get('output_url', '')
    else:
        return None

@app.route('/', methods=['GET', 'POST'])
def home():
    generated_logo_url = None

    if request.method == 'POST':
        text = request.form['text']
        style = request.form['style']

        if text and style:
            # Store the original text and style in the session
            session['original_text'] = text
            session['original_style'] = style
            generated_logo_url = generate_logo(text, style)
            flash('Logo generated successfully!', 'success')
        else:
            flash('Please provide both text and style.', 'error')

    return render_template('index.html', generated_logo_url=generated_logo_url)

@app.route('/edit_logo', methods=['GET', 'POST'])
def edit_logo():
    edited_logo_url = None

    if request.method == 'POST':
        # Get user input for logo editing (e.g., new text or style)
        new_text = request.form['new_text']
        new_style = request.form['new_style']
        
        # Retrieve the original text and style from the session
        original_text = session.get('original_text', '')
        original_style = session.get('original_style', '')
        
        # Call the DeepAI API again with the updated text and style
        edited_logo_url = generate_logo(original_text, original_style, new_text, new_style)
        
        flash('Logo edited successfully!', 'success')

    return render_template('edit_logo.html', edited_logo_url=edited_logo_url)

if __name__ == '__main__':
    app.run(debug=True)
