from marshmallow import Schema, fields
from .db import Base
from sqlalchemy import Column, Integer, String
from src.models.model import Model


class Plan(Model, Base):
    __tablename__ = "plan"
    nombre = Column(String(50), unique=True, nullable=False)
    descripcion = Column(String(250))
    vo2 = Column(Integer)

    def __init__(self, nombre, descripcion, vo2):
        Model.__init__(self)
        self.nombre = nombre
        self.descripcion = descripcion
        self.vo2 = vo2


class PlanSchema(Schema):
    id = fields.String()
    nombre = fields.String()
    descripcion = fields.String()
    vo2 = fields.Integer()
