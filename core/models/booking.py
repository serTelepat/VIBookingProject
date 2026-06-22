from pydantic import BaseModel
from typing import Optional
from datetime import date


class BookingDates(BaseModel):
    checkin: date
    checkout: date


class Booking(BaseModel):
    firstname: str
    lastname: str
    totalprice: int
    depositpaid: int
    bookingdates: BookingDates
    additionalneeds: Optional[str] = None


class BookingResponse(BaseModel):
    bookingid: int
    booking: Booking