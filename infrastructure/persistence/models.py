from sqlalchemy import Column, DateTime, Enum as SQLEnum, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from domain.order import OrderStatus
from infrastructure.persistence.base import Base


class OrderModel(Base):
    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column(String, nullable=False)
    item_id = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    status = Column(SQLEnum(OrderStatus, name="order_status"), nullable=False)
    idempotency_key = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=False)