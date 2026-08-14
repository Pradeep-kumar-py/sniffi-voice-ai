from core.table import Customer
from core.database import SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import select





async def get_customer_by_phone(phone: str):

    async with SessionLocal() as db:

        result = await db.execute(

            select(Customer).where(Customer.phone == phone)

        )

        return result.scalar_one_or_none()






async def save_customer(

    customer_id: int | None,

    phone: str,

    name: str | None,

    pet_name: str | None,

    pet_type: str | None,

    pet_age: str | None,

    address: str | None,

) -> Customer:

    async with SessionLocal() as db:

        customer = None

        # Existing customer

        if customer_id is not None:

            result = await db.execute(

                select(Customer).where(

                    Customer.id == customer_id

                )

            )

            customer = result.scalar_one_or_none()

        # Create customer

        if customer is None:

            customer = Customer(

                phone=phone,

                name=name,

                pet_name=pet_name,

                pet_type=pet_type,

                pet_age=pet_age,

                address=address,

                is_returning_customer=True,

            )

            db.add(customer)

        # Update existing customer

        else:

            customer.name = name

            customer.pet_name = pet_name

            customer.pet_type = pet_type

            customer.pet_age = pet_age

            customer.address = address

            customer.is_returning_customer = True

        await db.commit()

        # Populate generated ID / refreshed values

        await db.refresh(customer)

        return customer