# 🚗 Student Carpooling Platform

A simple web-based carpooling application for students built with Flask, HTML, CSS, and JavaScript.

## Features

✅ **User Authentication** - Sign up and login system
✅ **Offer Rides** - Drivers can post available rides
✅ **Request Rides** - Passengers can request to join rides
✅ **Real-time Chat** - Chat with driver and passengers about ride details
✅ **Ping Driver** - Send notifications to get driver's attention
✅ **Interactive Map** - View all rides on a Leaflet map
✅ **Profile Management** - View your profile and stats
✅ **My Rides Dashboard** - Track offered and requested rides
✅ **Accept/Reject Requests** - Drivers can manage passenger requests
✅ **Flexible Pricing** - Discuss and decide fare among yourselves

## Tech Stack

- **Backend**: Python + Flask
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript
- **Real-time**: Flask-SocketIO (WebSockets)
- **Map**: Leaflet.js

## Project Structure

```
carpooling-app/
│
├── app.py                 # Main Flask application
├── models.py              # Database models
├── requirements.txt       # Python dependencies
├── README.md             # This file
│
├── templates/            # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── signup.html
│   ├── dashboard.html
│   ├── offer_ride.html
│   ├── my_rides.html
│   ├── profile.html
│   ├── map.html
│   └── chat.html         # Real-time chat interface
│
└── static/               # Static files
    ├── css/
    │   └── style.css
    └── js/
```

## Installation & Setup

### Prerequisites
- Python 3.7 or higher installed
- pip (Python package manager)

### Step 1: Extract the Project
Extract the carpooling-app folder to your desired location.

### Step 2: Install Python Dependencies

Open terminal/command prompt in the project folder and run:

```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install Flask Flask-SQLAlchemy Werkzeug
```

### Step 3: Run the Application

```bash
python app.py
```

The application will start on `http://127.0.0.1:5000/`

### Step 4: Open in Browser

Go to: `http://localhost:5000`

## First Time Usage

1. **Sign Up**: Create a new account with your details
2. **Login**: Use your credentials to log in
3. **Offer a Ride**: Click "Offer Ride" and fill in the details (no need to set price!)
4. **View Dashboard**: See all available rides
5. **Request a Ride**: Click "Request Ride" on any available ride
6. **Ping Driver**: Use the "Ping Driver" button to get immediate attention
7. **Chat**: Once your request is accepted, use the chat to discuss details and fare
8. **Manage Rides**: Go to "My Rides" to see your offered rides and requests

## Database

The application uses SQLite database (`carpooling.db`) which is created automatically when you first run the app.

### Database Tables:
- **User**: Stores user information (name, email, password, phone)
- **Ride**: Stores ride details (origin, destination, time, seats)
- **RideRequest**: Stores ride requests from passengers
- **Message**: Stores chat messages for each ride

## Customization

### Real-time Chat & Ping Features

The app now includes **real-time chat** using WebSockets (Flask-SocketIO):
- **Chat Access**: Available to drivers and accepted passengers only
- **Ping Feature**: Anyone can ping a driver to get their attention (creates a highlighted message in chat)
- **Real-time Updates**: Messages appear instantly without page refresh
- **Auto-scroll**: Chat automatically scrolls to show new messages

**How it works:**
1. Once a ride request is accepted, both driver and passenger can access the chat
2. Click "Open Chat" from "My Rides" page
3. Type messages and discuss ride details, pickup location, and fare
4. Use the ping button from dashboard to notify the driver

### Change Map Location

Edit `templates/map.html` and update the coordinates:

```javascript
// Line 31: Change center coordinates to your campus location
const map = L.map('map').setView([YOUR_LAT, YOUR_LONG], 13);

// Lines 38-40: Update campus boundaries
const bounds = L.latLngBounds(
    L.latLng(SW_LAT, SW_LONG),  // Southwest corner
    L.latLng(NE_LAT, NE_LONG)   // Northeast corner
);
```

### Add More Locations

Edit the `locations` object in `templates/map.html`:

```javascript
const locations = {
    'Main Gate': [26.8467, 80.9462],
    'Library': [26.8487, 80.9482],
    'Your Location': [LAT, LONG],
    // Add more locations
};
```

### Change Secret Key

**Important**: Change the secret key in `app.py` for security:

```python
app.config['SECRET_KEY'] = 'your-unique-secret-key-here'
```

## Future Enhancements (You Can Add)

1. **ML Clustering**:
   - Install scikit-learn: `pip install scikit-learn`
   - Implement ride matching based on routes and preferences
   - Suggest optimal carpools based on historical data

2. **Email Notifications**:
   - Send emails when ride is accepted
   - Reminder emails before departure

3. **Reviews & Ratings**:
   - Add rating system for drivers and passengers
   - Calculate average ratings and display on profiles

4. **Payment Integration**:
   - Integrate payment gateway for seamless transactions
   - Split fare calculation helper

5. **Real-time Location**:
   - Track driver's current location on map
   - Estimated arrival time calculation

6. **File Sharing**:
   - Share images in chat (ride photos, vehicle details)
   - Voice messages support

## Common Issues & Solutions

### Issue: Port already in use
**Solution**: Change the port in `app.py`:
```python
app.run(debug=True, port=5001)  # Use a different port
```

### Issue: Database locked
**Solution**: Close the app and delete `carpooling.db`, then restart.

### Issue: Module not found
**Solution**: Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

## Learning Resources

- **Flask Documentation**: https://flask.palletsprojects.com/
- **Leaflet.js Docs**: https://leafletjs.com/
- **SQLAlchemy Docs**: https://docs.sqlalchemy.org/
- **HTML/CSS Basics**: https://developer.mozilla.org/

## Security Notes

⚠️ **This is a learning project**. For production use, you should:
- Use environment variables for sensitive data
- Implement proper password requirements
- Add CSRF protection
- Use HTTPS
- Add rate limiting
- Implement proper error handling
- Add input validation

## Contributing

Feel free to enhance this project! Some ideas:
- Add more features
- Improve the UI
- Add tests
- Implement the ML clustering
- Add mobile responsiveness

## License

This is a student learning project - free to use and modify!

## Support

If you run into issues:
1. Check if all dependencies are installed
2. Make sure Python 3.7+ is installed
3. Try deleting `carpooling.db` and restarting
4. Check the terminal for error messages

---

**Happy Carpooling! 🚗💨**

Made for learning purposes by a first-year CSE student.
