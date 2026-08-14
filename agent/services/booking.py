from sqlalchemy.ext.asyncio import AsyncSession

from core.database import SessionLocal
from core.table import Booking


async def create_booking(
    customer_id: int,
    service: str,
    preferred_date: str,
    preferred_time: str,
) -> Booking:

    async with SessionLocal() as db:

        booking = Booking(
            customer_id=customer_id,
            service=service,
            preferred_date=preferred_date,
            preferred_time=preferred_time,
        )

        db.add(booking)

        await db.commit()
        await db.refresh(booking)

        return booking