from config.db.database_config import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Table, Text
from sqlalchemy.orm import relationship


class Channels(Base):
    __tablename__ = 'channels'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(60))
    is_private = Column(Boolean, default=False)

    messages = relationship('Messages', back_populates='channel')


# Association table for the many-to-many relationship between Groups and Users
group_user_association = Table(
    'group_user_association',
    Base.metadata,
    Column('group_id', Integer, ForeignKey('groups.id')),
    Column('user_id', Integer, ForeignKey('users.id'))
)


class Groups(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(60))

    joined_users = relationship(
        'Users', secondary=group_user_association, back_populates='chat_groups')
    messages = relationship('Messages', back_populates='group')


class Messages(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True, index=True)
    message = Column(Text)
    sender_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    receiver_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    channel_id = Column(Integer, ForeignKey('channels.id'), nullable=False)
    group_id = Column(Integer, ForeignKey('groups.id'),
                      default=None, nullable=True)

    channel = relationship('Channels', back_populates='messages')
    group = relationship('Groups', back_populates='messages')
    sender = relationship('Users', foreign_keys=[
                          sender_id], back_populates='sent_messages')
    receiver = relationship('Users', foreign_keys=[
                            receiver_id], back_populates='received_messages')
