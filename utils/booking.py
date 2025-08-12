from datetime import time, timedelta, datetime
from typing import List

from db.models import Booking, Barber, Service



def check_barber_time(barber: Barber, booking_time_start: time, booking_time_end: time):
    if (
        (time(10, 0) <= booking_time_start)
          and 
        (booking_time_end <= barber.work_end_time)
    ):
        return True
    

def check_booking_intersection(
    bookings: List[Booking],
    booking_time_start: time, 
    booking_time_end: time,
    service: Service 
):
    for booking in bookings:
        existing_start = booking.time
        existing_end = (datetime.combine(datetime.today(), booking.time) +
                        timedelta(minutes=booking.service.duration_minute)).time()

        if booking_time_start < existing_end and booking_time_end > existing_start:
            return False
        
    return True
