from marshmallow import Schema, fields
from src.models.deportista import Deportista
from src.models.plan import Plan
from .db import Base
from sqlalchemy import UUID, Column, ForeignKey, Float, Boolean, String
from sqlalchemy.orm import Mapped, relationship
from src.models.model import Model


class PerfilAlimenticioDeportista(Model, Base):
    __tablename__ = "perfil_alimenticio_deportista"
    id_deportista = Column(UUID(as_uuid=True), ForeignKey('deportista.id'), primary_key=True)
    intorelancia_alergia = Column(Boolean)
    detalle_intolerancia_alergia = Column(String(50))
    vegano = Column(Boolean)
    objetivo_peso = Column(Float)

    deportista: Mapped['Deportista'] = relationship("Deportista", backref="perfil_alimenticio")

    def __init__(self, id_deportista, intorelancia_alergia, detalle_intolerancia_alergia, vegano, objetivo_peso):
        Model.__init__(self)
        self.id_deportista = id_deportista
        self.intorelancia_alergia = intorelancia_alergia
        self.detalle_intolerancia_alergia = detalle_intolerancia_alergia
        self.vegano = vegano
        self.objetivo_peso = objetivo_peso

class PerfilAlimenticioDeportistaSchema(Schema):
    id = fields.UUID()
    id_deportista = fields.UUID()
    intorelancia_alergia = fields.Bool()
    detalle_intolerancia_alergia = fields.Str()
    vegano = fields.Bool()
    objetivo_peso = fields.Float()