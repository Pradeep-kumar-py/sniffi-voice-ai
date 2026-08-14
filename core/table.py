from core.database import Base
from sqlalchemy import Boolean, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship



class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    phone: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False,
        index=True,
    )

    name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    pet_type: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )
    pet_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    pet_age: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    address: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    is_returning_customer: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )






class Booking(Base):

    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(

        Integer,

        primary_key=True,

        autoincrement=True,

    )

    customer_id: Mapped[int] = mapped_column(

        ForeignKey("customers.id", ondelete="CASCADE"),

        nullable=False,

        index=True,

    )

    service: Mapped[str] = mapped_column(

        String(100),

        nullable=False,

    )

    preferred_date: Mapped[str] = mapped_column(

        String(50),

        nullable=False,

    )

    preferred_time: Mapped[str] = mapped_column(

        String(50),

        nullable=False,

    )

    customer = relationship("Customer")