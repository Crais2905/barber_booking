from fastapi import Depends

from .connector import Connector
from db.models import Barber

class BarberCRUD(Connector):
    def __init__(self):
        super().__init__(Barber)