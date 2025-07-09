🌐 Conversion App
A simple web application to:

🔒 Log in with Google OAuth 2.0 (secure)

📏 Convert meters to feet

✨ Built with React + Flask

🚀 Features
✅ Google OAuth login (via secure backend session cookies)
✅ User profile display (name, email, photo)
✅ Meter-to-feet converter with instant results
✅ Responsive + clean UI
✅ Fully decoupled frontend (React) and backend (Flask)

🖥️ Tech Stack
Frontend	
React	

Backend	
Python (Flask)	

Auth
Google OAuth 2.0	

Misc
dotenv
CORS
requests

⚙️ Setup
🐍 Backend (Flask)
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

Create a .env file inside backend/:
FLASK_SECRET_KEY=your_flask_secret
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret

Run the server:

python app.py
Runs on: http://localhost:5000

⚛️ Frontend (React)
cd frontend
npm install
npm run dev
Runs on: http://localhost:5173

The React app communicates with the Flask API via http://localhost:5000.

🚀 Deployment
This app is easily deployable on platforms like:

Frontend	
Netlify / Vercel

Backend
Render / Railway / Heroku

Make sure to configure environment variables on your cloud platform (like Netlify / Render).

Keep your .env out of version control (.gitignore it).

📝 Example Environment File (backend/.env)
FLASK_SECRET_KEY=supersecret
GOOGLE_CLIENT_ID=xxxxxxxxx.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=xxxxxxxxxxxxxxxxxx