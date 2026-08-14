"""Generated Pipecat Flow: Untitled

This file was generated from the visual flow editor.

Functions are defined as pipecat-flows "direct functions": their schemas are
extracted automatically from each function's signature and docstring. Fill in
the function bodies to implement your flow logic.
"""


from typing import TypedDict

from pipecat.flows import (
    FlowManager,
    NodeConfig,
)

from agent.services.customer import get_customer_by_phone, save_customer
from agent.services.booking import create_booking as db_create_booking


# Type definitions
class UpdateBookingInformationResult(TypedDict):
    """Result type for the update_booking_information function."""
    name: str | None
    pet_name: str | None
    pet_type: str | None
    pet_age: str | None
    address: str | None
    service: str | None
    preferred_date: str | None
    preferred_time: str | None


# Functions for the Initial node
async def go_to_conversation(flow_manager: FlowManager) -> tuple[None, NodeConfig]:
    """
    Transitions from the initial greeting node to the conversation node
    
    after the customer has been greeted. Call this after completing
    
    the initial greeting.
    """
    return None, create_conversation_node()


# Functions for the conversation node
async def go_to_bookings(flow_manager: FlowManager) -> tuple[None, NodeConfig]:
    """Transition to the booking node when the customer wants to make a booking and all required booking information has been collected."""
    return None, create_booking_node()


async def update_booking_information(
    flow_manager: FlowManager,
    name: str | None = None,
    pet_name: str | None = None,
    pet_type: str | None = None,
    pet_age: str | None = None,
    address: str | None = None,
    service: str | None = None,
    preferred_date: str | None = None,
    preferred_time: str | None = None,
) -> tuple[UpdateBookingInformationResult, None]:
    """
    Update the booking information collected from the customer's latest response. Only provide fields that the customer has explicitly provided or corrected. Do not invent or assume information. This function does not create a booking or transition to another node.

    Args:
        name (str): ...
        pet_name (str): ...
        pet_type (str): ...
        pet_age (str): ...
        address (str): ...
        service (str): ...
        preferred_date (str): ...
        preferred_time (str): ...
    """
    # Only merge fields that were explicitly provided (non-None)
    updates: dict = {}
    if name is not None:
        updates["name"] = name
    if pet_name is not None:
        updates["pet_name"] = pet_name
    if pet_type is not None:
        updates["pet_type"] = pet_type
    if pet_age is not None:
        updates["pet_age"] = pet_age
    if address is not None:
        updates["address"] = address
    if service is not None:
        updates["service"] = service
    if preferred_date is not None:
        updates["preferred_date"] = preferred_date
    if preferred_time is not None:
        updates["preferred_time"] = preferred_time

    if updates:
        flow_manager.state.update(updates)

    # Return the current snapshot of all booking fields
    state = flow_manager.state
    result = UpdateBookingInformationResult(
        name=state.get("name"),
        pet_name=state.get("pet_name"),
        pet_type=state.get("pet_type"),
        pet_age=state.get("pet_age"),
        address=state.get("address"),
        service=state.get("service"),
        preferred_date=state.get("preferred_date"),
        preferred_time=state.get("preferred_time"),
    )
    return result, None


async def end_conversation_without_booking(flow_manager: FlowManager) -> tuple[None, NodeConfig]:
    """End the conversation when the customer clearly wants to finish the call."""
    return None, create_end_1_node()


# Functions for the booking node
async def end_conversation(flow_manager: FlowManager) -> tuple[None, NodeConfig]:
    """call this when booking is completed and it time to cut the phone call"""
    return None, create_end_node()


async def create_booking(flow_manager: FlowManager) -> tuple[None, None]:
    """Create the customer's booking after all required booking information has been collected and the customer has explicitly confirmed the details."""
    state = flow_manager.state

    # 1. Upsert the customer record so we always have an up-to-date DB entry
    customer = await save_customer(
        customer_id=state.get("customer_id"),
        phone=state.get("phone", ""),
        name=state.get("name"),
        pet_name=state.get("pet_name"),
        pet_type=state.get("pet_type"),
        pet_age=state.get("pet_age"),
        address=state.get("address"),
    )

    # Persist the resolved customer_id back into state
    flow_manager.state["customer_id"] = customer.id
    flow_manager.state["is_returning_customer"] = True

    # 2. Create the booking record
    booking = await db_create_booking(
        customer_id=customer.id,
        service=state.get("service", ""),
        preferred_date=state.get("preferred_date", ""),
        preferred_time=state.get("preferred_time", ""),
    )

    # 3. Mark booking as created in state
    flow_manager.state["booking_id"] = booking.id
    flow_manager.state["booking_created"] = True
    flow_manager.state["booking_confirmed"] = True

    return None, None


# Node creation functions
def create_initial_node() -> NodeConfig:
    """Create the Initial node."""
    return NodeConfig(
        name="initial",
        role_message="""You are Sniffi's AI voice receptionist.

Sniffi provides at-home veterinary care in Pune.

Available services:
- Regular Checkup
- Vaccination
- Dental Care
- Emergency Care

Your responsibilities:

1. Have a natural, friendly, and empathetic spoken phone conversation. Keep your responses concise and easy to listen to.
2. Collect the booking information required for an appointment.
3. Never ask for information that is already known.
4. If the caller provides multiple details in one response, capture all of them.
5. Never invent information.
6. If a value is unknown, leave it empty.
7. Ask only for ONE missing piece of information at a time to avoid overwhelming the caller.
8. Once every required field has been collected, summarize the details and ask the caller for confirmation before booking.
9. After the caller confirms, mark the booking as confirmed.

Required customer information:
- Owner name
- Pet type
- Pet age
- Address

Required booking information:
- Service
- Preferred date
- Preferred time

Respond naturally like a real human receptionist on a phone call. 
Do not use emojis, markdown, or long lists, as this will be read aloud by a text-to-speech engine. 
Do not mention internal state or implementation details.
""",
        task_messages=[
            {
                "role": "system",
                "content": """You are the friendly voice receptionist for Sniffi.

The customer's information has already been loaded before
this message is generated.

If an existing customer is available and their name is known,
welcome them by name.

If the customer is new, welcome them without using a name.

Ask how Sniffi can help them today.

Keep the greeting short and natural because this is a phone call.

IMPORTANT:
After you have delivered the greeting, immediately call the
`go_to_conversation` function.

Do not wait for the customer to respond before calling
`go_to_conversation`.

Do not ask for booking details in this node.
Do not attempt to create a booking.
Do not call any booking functions.

Your only responsibility in this node is:
1. Give the appropriate greeting.
2. Immediately call `go_to_conversation`.""",
            }
        ],
        functions=[go_to_conversation],
    )


def create_conversation_node() -> NodeConfig:
    """Create the conversation node."""
    return NodeConfig(
        name="conversation",
        task_messages=[
            {
                "role": "system",
                "content": """You are the Sniffi booking receptionist.

Have a natural conversation with the customer and understand what they need.

Your primary responsibility is to gather the information required for a booking:
* customer name
* pet name
* pet type
* pet age
* address
* requested service (Regular Checkup, Vaccination, Dental Care, Emergency Care)
* preferred date
* preferred time

Whenever the customer provides any booking details, immediately call `update_booking_information` to save the details.

Some customer information may already exist in the conversation state. Do not ask for information that is already known unless it needs confirmation or the customer wants to change it.

Ask for missing information naturally, one or two questions at a time. Do not interrogate the customer by asking for every field at once.

When the customer wants to make a booking and all required information has been collected, call the `go_to_bookings` function to proceed to the confirmation stage.

Do not call `go_to_bookings` if required information is still missing.

If the customer wants to end the call without booking, call `end_conversation_without_booking`.

Never create a booking directly from this node.""",
            }
        ],
        functions=[go_to_bookings, update_booking_information, end_conversation_without_booking],
    )


def create_booking_node() -> NodeConfig:
    """Create the booking node."""
    return NodeConfig(
        name="booking",
        task_messages=[
            {
                "role": "system",
                "content": """You are now in the booking confirmation stage.

The customer has requested to make a booking and all details should be collected.

Your workflow:
1. Review the collected booking details naturally with the customer:
   - Customer Name
   - Pet Name
   - Pet Type & Age
   - Address
   - Service
   - Preferred Date & Time
2. Ask the customer to explicitly confirm if all details are correct.
3. If the customer wants to modify details or info is missing, call `go_to_conversation`.
4. When the customer explicitly confirms the booking:
   - Call the `create_booking` function to create the booking in the system.
   - Inform the customer warmly that their appointment is booked.
   - Call the `end_conversation` function to complete the call and transition to the end node.

Do not call `create_booking` before the customer explicitly confirms.""",
            }
        ],
        functions=[end_conversation, create_booking, go_to_conversation],
    )


def create_end_node() -> NodeConfig:
    """Create the End node."""
    return NodeConfig(
        name="end",
        task_messages=[
            {
                "role": "system",
                "content": "Thank the user and end the conversation politely.",
            }
        ],
        post_actions=[
            {"type": "end_conversation"}
        ],
    )


def create_end_1_node() -> NodeConfig:
    """Create the End node."""
    return NodeConfig(
        name="end_1",
        task_messages=[
            {
                "role": "system",
                "content": "Thank the user and end the conversation politely.",
            }
        ],
        post_actions=[
            {"type": "end_conversation"}
        ],
    )


# FlowManager Setup
#
# Wire the generated nodes into your Pipecat bot:
#
# async def run_bot(transport: BaseTransport, runner_args: RunnerArguments):
#     stt = DeepgramSTTService(api_key=os.getenv("DEEPGRAM_API_KEY"))
#     tts = CartesiaTTSService(api_key=os.getenv("CARTESIA_API_KEY"))
#     llm = OpenAILLMService(api_key=os.getenv("OPENAI_API_KEY"))
#
#     context = LLMContext()
#     context_aggregator = LLMContextAggregatorPair(context)
#
#     pipeline = Pipeline([
#         transport.input(),
#         stt,
#         context_aggregator.user(),
#         llm,
#         tts,
#         transport.output(),
#         context_aggregator.assistant(),
#     ])
#
#     worker = PipelineWorker(pipeline, params=PipelineParams(enable_metrics=True))
#
#     # Initialize the FlowManager
#     flow_manager = FlowManager(
#         worker=worker,
#         llm=llm,
#         context_aggregator=context_aggregator,
#         transport=transport,
#         # global_functions=[...],
#     )
#
#     @transport.event_handler("on_client_connected")
#     async def on_client_connected(transport, client):
#         # Kick off the conversation with the initial node
#         await flow_manager.initialize(create_initial_node())
#
#     runner = WorkerRunner(handle_sigint=runner_args.handle_sigint)
#     await runner.add_workers(worker)
#     await runner.run()
