import enum
from datetime import datetime
from typing import Optional, Annotated
from sqlalchemy import String, MetaData, DateTime, ForeignKeyConstraint, Text, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, MappedAsDataclass, relationship

__all__ = ['Base', 'User', 'Post', 'Repeat', 'TaskTemplate', 'ScheduledTask']

class Base(MappedAsDataclass, DeclarativeBase):
    metadata = MetaData(naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_`%(constraint_name)s`",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    })


int_pk = Annotated[int, mapped_column(primary_key=True)]
dt = Annotated[datetime, mapped_column(DateTime)]
str30 = Annotated[str, mapped_column(String(30))]
str63 = Annotated[str, mapped_column(String(63))]
txt = Annotated[str, mapped_column(Text)]

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int_pk] = mapped_column(init=False)
    username: Mapped[str30] = mapped_column(unique=True)
    password: Mapped[str63] = mapped_column(repr=False)
    posts: Mapped[Optional["Post"]] = relationship()
    first_name: Mapped[Optional[str30]] = mapped_column(default=None)
    last_name: Mapped[Optional[str30]] = mapped_column(default=None)
    email_address: Mapped[Optional[str63]] = mapped_column(default=None)


class Post(Base):
    __tablename__ = 'posts'

    id: Mapped[int_pk] = mapped_column(init=False)
    title: Mapped[str30] = mapped_column()
    body: Mapped[txt] = mapped_column()
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    author_name: Mapped[str30] = mapped_column()
    created: Mapped[dt] = mapped_column(default=datetime.now())


class Repeat(enum.Enum):
    HOURLY = 'hourly'
    DAILY = 'daily'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'
    SCHEDULED = 'scheduled'
    ONCE = 'once'


class TaskTemplate(Base):
    __tablename__ = 'task_templates'

    id: Mapped[int_pk] = mapped_column(init=False)
    task_template_name: Mapped[str30] = mapped_column(unique=True)
    task_template_repeat: Mapped[Repeat] = mapped_column()
    task_template_description: Mapped[Optional[txt]] = mapped_column(default=None)


class ScheduledTask(Base):
    __tablename__ = 'scheduled_tasks'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id']),
        ForeignKeyConstraint(['task_template_id'], ['task_templates.id'])
    )

    id: Mapped[int_pk] = mapped_column(init=False)
    user_id: Mapped[int] = mapped_column()
    user: Mapped['User'] = relationship()
    task_template_id: Mapped[int] = mapped_column()
    task_template: Mapped['TaskTemplate'] = relationship()
    scheduled_start: Mapped[Optional[dt]] = mapped_column(default=None)
    scheduled_end: Mapped[Optional[dt]] = mapped_column(default=None)