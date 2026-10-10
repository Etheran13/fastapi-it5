"""Data models used to validate API input and output."""

from typing import Literal
from pydantic import BaseModel, Field


class RoomInput(BaseModel):
    """Fields users send when creating a room."""
    name: str = Field(min_length=1)
    capacity: int = Field(ge=1)

    @staticmethod
    def list_rooms(database_connection):
        with database_connection() as connection:
            rows = connection.execute("SELECT id, name, capacity FROM rooms ORDER BY id").fetchall()
        return rows

    @staticmethod
    def create_room(room_input, database_connection):
        with database_connection() as connection:
            cursor = connection.execute(
                "INSERT INTO rooms (name, capacity) VALUES (?, ?)",
                (room_input.name, room_input.capacity),
            )
            row = connection.execute(
                "SELECT id, name, capacity FROM rooms WHERE id = ?", (cursor.lastrowid,)
            ).fetchone()
        return row

    @staticmethod
    def get_room(room_id, database_connection):
        with database_connection() as connection:
            row = connection.execute(
                "SELECT id, name, capacity FROM rooms WHERE id = ?", (room_id,)
            ).fetchone()
        return row


class Room(RoomInput):
    """A room record returned by the API."""
    id: int


class BookingInput(BaseModel):
    """Fields users can send when creating or updating a booking."""
    name: str = Field(min_length=1)
    amount_of_guests: int = Field(ge=1)
    payment_status: Literal["fully paid", "downpayment only"]
    room_id: int

    @staticmethod
    def list_bookings(database_connection):
        with database_connection() as connection:
            rows = connection.execute(
                "SELECT booking_number, name, amount_of_guests, payment_status, room_id FROM bookings ORDER BY booking_number"
            ).fetchall()
        return rows

    @staticmethod
    def create_booking(booking_input, database_connection):
        with database_connection() as connection:
            cursor = connection.execute(
                "INSERT INTO bookings (name, amount_of_guests, payment_status, room_id) VALUES (?, ?, ?, ?)",
                (booking_input.name, booking_input.amount_of_guests, booking_input.payment_status, booking_input.room_id),
            )
            row = connection.execute(
                "SELECT booking_number, name, amount_of_guests, payment_status, room_id FROM bookings WHERE booking_number = ?", 
                (cursor.lastrowid,)
            ).fetchone()
        return row

    @staticmethod
    def get_booking(booking_number, database_connection):
        with database_connection() as connection:
            row = connection.execute(
                "SELECT booking_number, name, amount_of_guests, payment_status, room_id FROM bookings WHERE booking_number = ?", 
                (booking_number,)
            ).fetchone()
        return row

    @staticmethod
    def update_booking(booking_number, booking_input, database_connection):
        with database_connection() as connection:
            cursor = connection.execute(
                "UPDATE bookings SET name = ?, amount_of_guests = ?, payment_status = ?, room_id = ? WHERE booking_number = ?",
                (booking_input.name, booking_input.amount_of_guests, booking_input.payment_status, booking_input.room_id, booking_number),
            )
            row = connection.execute(
                "SELECT booking_number, name, amount_of_guests, payment_status, room_id FROM bookings WHERE booking_number = ?", 
                (booking_number,)
            ).fetchone()
        return row

    @staticmethod
    def delete_booking(booking_number, database_connection):
        with database_connection() as connection:
            cursor = connection.execute(
                "DELETE FROM bookings WHERE booking_number = ?", (booking_number,)
            )


class Booking(BookingInput):
    """A booking record returned by the API."""
    booking_number: int