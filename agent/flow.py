"""Generated Pipecat Flow: Untitled

This file was generated from the visual flow editor.

Functions are defined as pipecat-flows "direct functions": their schemas are
extracted automatically from each function's signature and docstring. Fill in
the function bodies to implement your flow logic.
"""


from pipecat.flows import FlowManager, NodeConfig

# Functions for the Initial node
async def go_to_convertation(flow_manager: FlowManager) -> tuple[None, NodeConfig]:
    """Handle the go_to_convertation function."""
    # TODO: Implement function logic
    # Update flow_manager.state as needed
    return None, create_convertation_node()


# Functions for the convertation node
async def end_convertation(flow_manager: FlowManager) -> tuple[None, NodeConfig]:
    """Handle the end_convertation function."""
    # TODO: Implement function logic
    # Update flow_manager.state as needed
    return None, create_end_node()


# Node creation functions
def create_initial_node() -> NodeConfig:
    """Create the Initial node."""
    return NodeConfig(
        name="initial",
        role_message="""You are a friendly AI receptionist for a business.

Speak naturally, clearly, and professionally.
Your responses will be converted to speech, so keep them concise and conversational.""",
        functions=[go_to_convertation],
        pre_actions=[
            {"type": "tts_say", "text": "Hi, thanks for calling.  How can I help you today?"}
        ],
    )


def create_convertation_node() -> NodeConfig:
    """Create the convertation node."""
    return NodeConfig(
        name="convertation",
        task_messages=[
            {
                "role": "system",
                "content": """Have a natural conversation with the customer.

Listen carefully to what the customer says and respond naturally and helpfully.

Ask relevant follow-up questions when necessary.

For this initial version, do not perform any booking, database, or external operations.

If the customer clearly indicates that they are finished, says goodbye, or wants to end the call, call the `end_conversation` function.""",
            }
        ],
        functions=[end_convertation],
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
