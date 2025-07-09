import os
import json
import requests
from flask import Flask, session, redirect, url_for, request, jsonify
from google_auth_oauthlib.flow import Flow
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "some_dev_secret")

# CORS to allow React on a different port to send cookies
CORS(app, supports_credentials=True)

# OAuth config
CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile"
]

CLIENT_CONFIG = {
    "web": {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "redirect_uris": ["https://conversion-e59b.onrender.com/callback"]
    }
}

# -----------------------
# Routes
# -----------------------

@app.route('/')
def index():
    print(">>> / called")
    if 'credentials' not in session:
        print("No credentials found in session.")
        return '<a href="/login">Login with Google</a>'
    
    creds = session['credentials']
    print("Found credentials in session:", creds)

    headers = {'Authorization': f"Bearer {creds['token']}"}
    userinfo = requests.get(
        "https://www.googleapis.com/oauth2/v1/userinfo", headers=headers
    ).json()
    print("Fetched userinfo:", json.dumps(userinfo, indent=2))

    return f'''
        <h1>You are logged in as {userinfo.get("email")}</h1>
        <img src="{userinfo.get("picture")}" alt="profile picture"><br>
        <a href="/logout">Logout</a>
    '''


@app.route('/login')
def login():
    print(">>> /login called")
    flow = Flow.from_client_config(
        CLIENT_CONFIG,
        scopes=SCOPES,
        redirect_uri=url_for('callback', _external=True)
    )
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent'
    )
    print("Generated authorization_url:", authorization_url)
    session['state'] = state
    return redirect(authorization_url)


@app.route('/callback')
def callback():
    print(">>> /callback called")
    state = session.get('state')
    print("Session state:", state)
    print("Request URL:", request.url)

    flow = Flow.from_client_config(
        CLIENT_CONFIG,
        scopes=SCOPES,
        state=state,
        redirect_uri=url_for('callback', _external=True)
    )

    try:
        flow.fetch_token(authorization_response=request.url)
    except Exception as e:
        print("Error fetching token:", e)
        return f"<h1>Authentication failed</h1><p>{str(e)}</p>"

    credentials = flow.credentials
    print("Fetched credentials:", credentials.to_json())

    session['credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }
    return redirect("https://conversion-1-g0am.onrender.com")  # direct back to React after login


@app.route('/logout')
def logout():
    print(">>> /logout called")
    session.clear()
    return redirect(url_for('index'))


# ---------------------------
# API for React Frontend
# ---------------------------

@app.route('/api/profile')
def api_profile():
    print(">>> /api/profile called")
    if 'credentials' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    creds = session['credentials']
    headers = {'Authorization': f"Bearer {creds['token']}"}
    userinfo = requests.get(
        "https://www.googleapis.com/oauth2/v1/userinfo", headers=headers
    ).json()
    print("API fetched userinfo:", json.dumps(userinfo, indent=2))
    return jsonify(userinfo)


@app.route('/api/logout')
def api_logout():
    print(">>> /api/logout called")
    session.clear()
    return jsonify({"message": "Logged out"})

@app.route('/api/convert', methods=['POST'])
def api_convert():
    print(">>> /api/convert called")
    if 'credentials' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    if not data or 'meters' not in data:
        return jsonify({'error': 'Missing "meters" field'}), 400

    text_input = str(data['meters'])
    import re
    match = re.search(r'[-+]?\d*\.?\d+', text_input)
    if not match:
        return jsonify({'error': 'No numeric value found in input'}), 400

    meters = float(match.group())
    feet = meters * 3.28084
    print(f"Converted {meters} meters -> {feet} feet")

    return jsonify({'meters': meters, 'feet': round(feet, 2)})

# ----------------------------
# Start the app
# ----------------------------

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
