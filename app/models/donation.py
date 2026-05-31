from __future__ import annotations

from datetime import datetime

from sqlalchemy import Text, ForeignKey, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import InvestmentBase
from app.models.user import User


class Donation(InvestmentBase):
    __tablename__ = 'donation'

    id: Mapped[int] = mapped_column(primary_key=True)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)

    create_date: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('user.id', name='fk_donation_user_id_user'),
        nullable=False,
    )
    user: Mapped['User'] = relationship('User', lazy='selectin')
