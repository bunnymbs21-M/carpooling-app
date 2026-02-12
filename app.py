import os
from datetime import datetime

from flask import (
    Flask,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_socketio import SocketIO, emit, join_room, leave_room

# Make sure your models.py file is in the same folder!
from models import Message, Ride, RideRequest, User, db

app = Flask(__name__)
app.config["SECRET_KEY"] = "spsu-unihop-secret-key-2026"  # Changed for security
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///carpooling.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Create tables automatically if they don't exist
with app.app_context():
    db.create_all()


# --- AUTHENTICATION ROUTES ---

@app.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return render_template("index.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        phone = request.form["phone"]

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered!", "error")
            return redirect(url_for("signup"))

        new_user = User(name=name, email=email, phone=phone)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully! Please login.", "success")
        return redirect(url_for("login"))

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session["user_id"] = user.id
            session["user_name"] = user.name
            flash("Login successful!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid email or password!", "error")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully!", "success")
    return redirect(url_for("index"))


# --- CORE APP ROUTES ---

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Get all available rides, sorted by newest first
    rides = (
        Ride.query.filter_by(status="available")
        .order_by(Ride.departure_time.desc())
        .all()
    )
    return render_template("dashboard.html", rides=rides)


@app.route("/offer-ride", methods=["GET", "POST"])
def offer_ride():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        origin = request.form["origin"]
        destination = request.form["destination"]
        departure_time = datetime.strptime(
            request.form["departure_time"], "%Y-%m-%dT%H:%M"
        )
        seats_available = int(request.form["seats_available"])

        new_ride = Ride(
            driver_id=session["user_id"],
            origin=origin,
            destination=destination,
            departure_time=departure_time,
            seats_available=seats_available,
        )

        db.session.add(new_ride)
        db.session.commit()

        # --- LIVE FEED LOGIC START ---
        # We create a dictionary of the ride data to send to everyone instantly
        ride_payload = {
            "id": new_ride.id,
            "origin": new_ride.origin,
            "destination": new_ride.destination,
            "date": new_ride.departure_time.strftime("%d %b"),  # e.g., 12 Feb
            "time": new_ride.departure_time.strftime("%I:%M %p"), # e.g., 02:30 PM
            "seats": new_ride.seats_available,
            "driver_name": session["user_name"],
            "driver_id": session["user_id"]
        }
        
        # Broadcast this payload to the 'new_ride_notification' channel
        socketio.emit("new_ride_notification", ride_payload)
        # --- LIVE FEED LOGIC END ---

        flash("Ride offered successfully! It is now live on the dashboard.", "success")
        return redirect(url_for("my_rides"))

    return render_template("offer_ride.html")


@app.route("/request-ride/<int:ride_id>", methods=["POST"])
def request_ride(ride_id):
    if "user_id" not in session:
        return jsonify({"error": "Not logged in"}), 401

    ride = Ride.query.get_or_404(ride_id)

    if ride.driver_id == session["user_id"]:
        return jsonify({"error": "Cannot request your own ride"}), 400

    existing_request = RideRequest.query.filter_by(
        ride_id=ride_id, passenger_id=session["user_id"]
    ).first()

    if existing_request:
        return jsonify({"error": "Already requested this ride"}), 400

    new_request = RideRequest(ride_id=ride_id, passenger_id=session["user_id"])
    db.session.add(new_request)
    db.session.commit()

    return jsonify({"success": "Ride requested successfully"})


@app.route("/my-rides")
def my_rides():
    if "user_id" not in session:
        return redirect(url_for("login"))

    my_offered_rides = Ride.query.filter_by(driver_id=session["user_id"]).all()
    my_requests = RideRequest.query.filter_by(passenger_id=session["user_id"]).all()

    return render_template(
        "my_rides.html", offered_rides=my_offered_rides, requested_rides=my_requests
    )


@app.route("/profile")
def profile():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user = User.query.get(session["user_id"])
    return render_template("profile.html", user=user)


@app.route("/accept-request/<int:request_id>", methods=["POST"])
def accept_request(request_id):
    if "user_id" not in session:
        return jsonify({"error": "Not logged in"}), 401

    ride_request = RideRequest.query.get_or_404(request_id)
    ride = Ride.query.get(ride_request.ride_id)

    if ride.driver_id != session["user_id"]:
        return jsonify({"error": "Not authorized"}), 403

    if ride.seats_available <= 0:
        return jsonify({"error": "No seats available"}), 400

    ride_request.status = "accepted"
    ride.seats_available -= 1

    if ride.seats_available == 0:
        ride.status = "full"

    db.session.commit()

    return jsonify({"success": "Request accepted"})


@app.route("/map")
def map_view():
    if "user_id" not in session:
        return redirect(url_for("login"))

    rides_objects = Ride.query.filter_by(status="available").all()
    rides_data = []
    for ride in rides_objects:
        rides_data.append(
            {
                "origin": ride.origin,
                "destination": ride.destination,
                "driver": {"name": ride.driver.name},
                "departure_time": ride.departure_time.isoformat(),
                "seats_available": ride.seats_available,
            }
        )

    return render_template("map.html", rides=rides_data)


# --- CHAT & REAL-TIME ROUTES ---

@app.route("/chat/<int:ride_id>")
def chat(ride_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    ride = Ride.query.get_or_404(ride_id)

    is_driver = ride.driver_id == session["user_id"]
    is_passenger = (
        RideRequest.query.filter_by(
            ride_id=ride_id, passenger_id=session["user_id"], status="accepted"
        ).first()
        is not None
    )

    if not (is_driver or is_passenger):
        flash("You must be part of this ride to access the chat!", "error")
        return redirect(url_for("dashboard"))

    messages = (
        Message.query.filter_by(ride_id=ride_id).order_by(Message.created_at).all()
    )

    return render_template("chat.html", ride=ride, messages=messages)


@app.route("/api/messages/<int:ride_id>")
def get_messages(ride_id):
    if "user_id" not in session:
        return jsonify({"error": "Not logged in"}), 401

    messages = (
        Message.query.filter_by(ride_id=ride_id).order_by(Message.created_at).all()
    )

    return jsonify(
        {
            "messages": [
                {
                    "id": msg.id,
                    "sender_name": msg.sender.name,
                    "sender_id": msg.sender_id,
                    "message": msg.message,
                    "created_at": msg.created_at.strftime("%I:%M %p"),
                }
                for msg in messages
            ]
        }
    )


@app.route("/ping-driver/<int:ride_id>", methods=["POST"])
def ping_driver(ride_id):
    if "user_id" not in session:
        return jsonify({"error": "Not logged in"}), 401

    ride = Ride.query.get_or_404(ride_id)
    user = User.query.get(session["user_id"])

    ping_message = Message(
        ride_id=ride_id,
        sender_id=session["user_id"],
        message=f"🔔 {user.name} is pinging the driver! Please respond.",
    )

    db.session.add(ping_message)
    db.session.commit()

    socketio.emit(
        "new_message",
        {
            "ride_id": ride_id,
            "sender_name": user.name,
            "sender_id": user.id,
            "message": ping_message.message,
            "created_at": ping_message.created_at.strftime("%I:%M %p"),
            "is_ping": True,
        },
        room=f"ride_{ride_id}",
    )

    return jsonify({"success": "Driver pinged successfully!"})


# --- SOCKET.IO EVENTS ---

@socketio.on("join_ride")
def handle_join_ride(data):
    ride_id = data["ride_id"]
    join_room(f"ride_{ride_id}")
    emit(
        "user_joined",
        {"message": f"{session.get('user_name', 'A user')} joined the chat"},
        room=f"ride_{ride_id}",
    )


@socketio.on("leave_ride")
def handle_leave_ride(data):
    ride_id = data["ride_id"]
    leave_room(f"ride_{ride_id}")


@socketio.on("send_message")
def handle_send_message(data):
    if "user_id" not in session:
        return

    ride_id = data["ride_id"]
    message_text = data["message"]

    new_message = Message(
        ride_id=ride_id, sender_id=session["user_id"], message=message_text
    )

    db.session.add(new_message)
    db.session.commit()

    emit(
        "new_message",
        {
            "ride_id": ride_id,
            "sender_name": session["user_name"],
            "sender_id": session["user_id"],
            "message": message_text,
            "created_at": new_message.created_at.strftime("%I:%M %p"),
        },
        room=f"ride_{ride_id}",
    )


if __name__ == "__main__":
    socketio.run(app, debug=True)