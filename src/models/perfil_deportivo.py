from marshmallow import Schema, fields
from src.models.deportista import Deportista
from .db import Base
from sqlalchemy import UUID, Column, ForeignKey, Float, Boolean, String, Integer
from sqlalchemy.orm import Mapped, relationship
from src.models.model import Model


class PerfilDeportivo(Model, Base):
    __tablename__ = "perfil_deportivo"
    id_deportista = Column(UUID(as_uuid=True), ForeignKey('deportista.id'), primary_key=True)
    dias_semana_practica = Column(Integer)
    tiempo_practica = Column(Integer)
    VO2max_actual = Column(Float)
    FTP_actual = Column(Float)
    lesion_molestia_incapacidad = Column(Boolean)
    detalle_lesion_molestia_incapacidad = Column(String(200))

    deportista: Mapped['Deportista'] = relationship("Deportista", backref="perfil_deportivo")

    def __init__(self, id_deportista, dias_semana_practica, tiempo_practica, VO2max_actual, FTP_actual, lesion_molestia_incapacidad, detalle_lesion_molestia_incapacidad):
        Model.__init__(self)
        self.id_deportista = id_deportista
        self.dias_semana_practica = dias_semana_practica
        self.tiempo_practica = tiempo_practica
        self.VO2max_actual = VO2max_actual
        self.FTP_actual = FTP_actual
        self.lesion_molestia_incapacidad = lesion_molestia_incapacidad
        self.detalle_lesion_molestia_incapacidad = detalle_lesion_molestia_incapacidad


class PerfilDeportivoSchema(Schema):
    id = fields.UUID()
    id_deportista = fields.UUID()
    dias_semana_practica = fields.Int()
    tiempo_practica = fields.Int()
    VO2max_actual = fields.Float()
    FTP_actual = fields.Float()
    lesion_molestia_incapacidad = fields.Bool()
    detalle_lesion_molestia_incapacidad = fields.Str()