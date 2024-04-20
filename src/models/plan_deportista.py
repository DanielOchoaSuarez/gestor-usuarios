from src.models.deportista import Deportista
from src.models.plan import Plan
from .db import Base
from sqlalchemy import UUID, Column, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from src.models.model import Model


class PlanDeportista(Model, Base):
    __tablename__ = "plan_deportista"
    id_plan = Column(UUID(as_uuid=True), ForeignKey('plan.id'), primary_key=True)
    id_deportista = Column(UUID(as_uuid=True), ForeignKey('deportista.id'), primary_key=True)

    plan: Mapped['Plan'] = relationship("Plan", backref="deportistas")
    deportista: Mapped['Deportista'] = relationship("Deportista", backref="planes")

    def __init__(self, id_plan, id_deportista):
        Model.__init__(self)
        self.id_plan = id_plan
        self.id_deportista = id_deportista
