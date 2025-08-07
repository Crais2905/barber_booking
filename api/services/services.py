from fastapi import Depends

from .connector import Connector
from db.models import Service

class ServicesCRUD(Connector):
    def __init__(self):
        super().__init__(Service)
