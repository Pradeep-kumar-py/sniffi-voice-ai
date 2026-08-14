from typing import TypedDict


class BookingState(TypedDict):
    # Session
    phone: str
    customer_id: int | None
    is_returning_customer: bool

    # Customer Information
    name: str | None
    pet_name:str | None
    pet_type: str | None
    pet_age: str | None
    address: str | None

    # Booking Information
    booking_id: int | None
    service: str | None
    preferred_date: str | None
    preferred_time: str | None

    # Confirmation
    booking_confirmed: bool
    booking_created: bool


def create_initial_state(phone: str) -> BookingState:
    return {
        "phone": phone,
        "customer_id": None,
        "is_returning_customer": False,

        "name": None,
        "pet_name": None,
        "pet_type": None,
        "pet_age": None,
        "address": None,

        "booking_id": None,
        "service": None,
        "preferred_date": None,
        "preferred_time": None,

        "booking_confirmed": False,
        "booking_created": False,
    }