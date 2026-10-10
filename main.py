"""Create the FastAPI app and connect its route modules."""

from fastapi import FastAPI, HTTPException

from app.database import database_connection, initialize_database
from app.models import Booking, BookingInput, Room, RoomInput

app = FastAPI(title="Booking System API")


@app.get("/")
def home():
    return {"message": "Welcome to the Booking System!"}


# --- Room Endpoints ---

@app.get("/rooms")
def get_rooms():
    result = Room.list_rooms(database_connection=database_connection)
    return {"rooms": result}

@app.post("/room")
def create_room(room: RoomInput):
    result = Room.create_room(
        room_input=room, database_connection=database_connection
    )
    return {"room": result}


# --- Booking Endpoints ---

@app.get("/bookings")
def get_bookings():
    result = Booking.list_bookings(database_connection=database_connection)
    return {"bookings": result}


@app.get("/bookings/{booking_number}")
def get_booking(booking_number: int):
    result = Booking.get_booking(
        booking_number=booking_number, database_connection=database_connection
    )
    if not result:
        raise HTTPException(status_code=404, detail="Booking not found")
    return {"booking": result}


@app.post("/booking")
def create_booking(booking: BookingInput):
    # Transactional Logic: Capacity Verification
    room = Room.get_room(booking.room_id, database_connection=database_connection)
    
    if not room:
        raise HTTPException(status_code=404, detail="The requested room_id does not exist.")
        
    if booking.amount_of_guests > room["capacity"]:
        raise HTTPException(
            status_code=400, 
            detail=f"Transaction failed: {booking.amount_of_guests} guests exceeds the maximum capacity ({room['capacity']}) for {room['name']}."
        )

    result = Booking.create_booking(
        booking_input=booking, database_connection=database_connection
    )
    return {"booking": result}


@app.put("/booking/{booking_number}")
def edit_booking(booking_number: int, booking: BookingInput):
    # Enforce capacity checks on edits as well
    room = Room.get_room(booking.room_id, database_connection=database_connection)
    if not room:
        raise HTTPException(status_code=404, detail="The requested room_id does not exist.")
    if booking.amount_of_guests > room["capacity"]:
        raise HTTPException(status_code=400, detail="Transaction failed: Guest amount exceeds room capacity.")

    result = Booking.update_booking(
        booking_number=booking_number,
        booking_input=booking,
        database_connection=database_connection,
    )
    return {"booking": result}


@app.delete("/booking/{booking_number}")
def delete_booking(booking_number: int):
    Booking.delete_booking(
        booking_number=booking_number, database_connection=database_connection
    )
    return {"message": "Booking deleted successfully"}


initialize_database()