from sqlalchemy import Column, DateTime, Enum as SQLEnum, Integer, String, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB

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
    payment_id = Column(String, nullable=True)




class OutboxModel(Base):
    __tablename__ = "outbox"

    id = Column(UUID(as_uuid=True), primary_key=True)
    topic = Column(String, nullable=False)
    payload = Column(JSONB, nullable=False)
    is_sent = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), nullable=False)



class InboxModel(Base):
    __tablename__ = "inbox"

    id = Column(UUID(as_uuid=True), primary_key=True)
    event_key = Column(String, nullable=False, unique=True)
    processed_at = Column(DateTime(timezone=True), nullable=False)