import os
import json
import logging
from flask import Flask, render_template, request, jsonify, redirect, url_for
from email_service import send_trail_email, send_discount_email

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET")

# Ensure the static/assets directory exists
os.makedirs('static/assets', exist_ok=True)

# Copy the logo to the static assets directory
import shutil
shutil.copy('attached_assets/logo_sport_outdoor.png', 'static/assets/logo_sport_outdoor_langueux.png')

# Load trails data based on activity type
def load_trails(activity: str):
    """
    Load trails data based on activity type
    """
    try:
        activity_map = {
            'running': 'trails_running.json',
            'trail': 'trails_trail.json',
            'hiking': 'trails_hiking.json'
        }

        json_file = activity_map.get(activity)
        if not json_file:
            logger.error(f"Invalid activity type: {activity}")
            return {"trails": []}

        with open(f'static/data/{json_file}', 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading trails data: {e}")
        return {"trails": []}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/error')
def error():
    discount_code = request.args.get('discount_code', 'SPORT10')
    return render_template('error.html', discount_code=discount_code)

@app.route('/submit', methods=['POST'])
def submit():
    try:
        logger.debug("Received form submission")
        # Get form data
        location = request.form.get('location')
        activity = request.form.get('activity')
        difficulty = request.form.get('difficulty')
        distance = int(request.form.get('distance'))
        landscape = request.form.get('landscape')
        email = request.form.get('email')

        logger.debug(f"Form data: location={location}, activity={activity}, difficulty={difficulty}, distance={distance}, landscape={landscape}, email={email}")

        # Validate input
        if not all([location, activity, difficulty, distance, landscape, email]):
            logger.error("Missing required fields")
            return jsonify({'success': False, 'error': 'Tous les champs sont requis'})

        # Load trails for the specific activity
        trails_data = load_trails(activity)
        matched_trail = None

        for trail in trails_data['trails']:
            if (trail['location'] == location and
                trail['difficulty_level'] == difficulty and
                abs(trail['distance'] - distance) <= 5 and
                trail.get('landscape', '') == landscape):
                matched_trail = trail
                break

        logger.debug(f"Matched trail: {matched_trail}")

        # Generate discount code regardless of match
        discount_code = f"SPORT{hash(email) % 1000:03d}"

        if not matched_trail:
            logger.info("No matching trail found, sending 10% discount")
            # Send 10% discount code by email
            email_sent = send_discount_email(
                email=email,
                discount_code=discount_code,
                discount_percentage=10
            )

            if not email_sent:
                logger.error("Failed to send discount email")
                return jsonify({'success': False, 'error': "Erreur lors de l'envoi de l'email"})

            return jsonify({
                'success': False, 
                'redirect': f'/error?discount_code={discount_code}'
            })

        logger.info("Matching trail found, sending trail info and 5% discount")
        # Send email with trail and 5% discount code
        success = send_trail_email(
            email=email,
            trail_data=matched_trail,
            discount_code=discount_code
        )

        if not success:
            logger.error("Failed to send trail email")
            return jsonify({'success': False, 'error': "Erreur lors de l'envoi de l'email"})

        return jsonify({'success': True})

    except Exception as e:
        logger.error(f"Error in submit: {e}")
        return jsonify({'success': False, 'error': 'Une erreur est survenue'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)