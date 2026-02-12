# 🚀 Quick Start Guide

## Get Started in 3 Steps!

### Step 1: Install Python Dependencies
Open terminal in this folder and run:
```bash
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
python app.py
```

### Step 3: Open in Browser
Go to: http://localhost:5000

---

## Your First Ride

1. **Sign Up** with your name, email, phone, and password
2. **Login** with your credentials
3. **Offer a Ride** (no need to set price - discuss with passengers!)
4. **Request a Ride** from the dashboard
5. **Ping Driver** to get their attention quickly
6. **Chat** with other riders once request is accepted
7. **View Map** to see all rides on an interactive map

---

## File Structure Overview

- `app.py` - Main Flask application (routes and logic)
- `models.py` - Database models (User, Ride, RideRequest)
- `templates/` - All HTML pages
- `static/css/` - Styling
- `requirements.txt` - Python packages needed

---

## Important Notes

🔑 **Security**: Change the SECRET_KEY in `app.py` before deploying

📍 **Map Location**: Update coordinates in `templates/map.html` to match your campus

💾 **Database**: The SQLite database (`carpooling.db`) is created automatically

---

## Need Help?

Check the main README.md file for:
- Detailed setup instructions
- Customization guide
- Troubleshooting tips
- Future enhancement ideas

Happy Coding! 🎉
