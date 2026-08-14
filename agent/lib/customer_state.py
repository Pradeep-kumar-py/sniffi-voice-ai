from agent.services.customer import get_customer_by_phone
from agent.state import BookingState
async def load_customer_state(phone: str, state: BookingState) -> BookingState:
    customer = await get_customer_by_phone(phone)

    if not customer:
        return state

    state.update({
        "customer_id": customer.id,
        "is_returning_customer": True,
        "name": customer.name,
        "pet_name": customer.pet_name,
        "pet_type": customer.pet_type,
        "pet_age": customer.pet_age,
        "address": customer.address,
    })

    return state