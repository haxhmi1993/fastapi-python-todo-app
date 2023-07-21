from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from config.db.database_config import Base
from modules.messaging.models import group_user_association


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    phone_number = Column(String)

    todos = relationship('Todos', back_populates='owner')
    chat_groups = relationship(
        'Groups', secondary=group_user_association, back_populates='joined_users')
    sent_messages = relationship(
        'Messages', foreign_keys='Messages.sender_id', back_populates='sender')
    received_messages = relationship(
        'Messages', foreign_keys='Messages.receiver_id', back_populates='receiver')
