from deepgram.requests import create_project_distribution_credentials_v1response_distribution_credentials
from core.config import settings
from fastapi import WebSocket
from xml.sax.saxutils import escape

from pipecat.serializers.vobiz import (
    VobizFrameSerializer,
    parse_vobiz_start,
)

from pipecat.transports.websocket.fastapi import (
    FastAPIWebsocketParams,
    FastAPIWebsocketTransport,
)




def get_vobiz_public_url() -> str:

    public_url = settings.vobiz_public_url

    if not public_url:
        raise RuntimeError(
            "VOBIZ_PUBLIC_URL is not configured. "
            "Set it to your public HTTPS URL."
        )

    return public_url.rstrip("/")


def build_vobiz_answer_xml(phone: str) -> str:
    """
    XML returned to Vobiz when a call is answered.

    This tells Vobiz to create a bidirectional WebSocket
    connection to our Pipecat bot.
    """

    public_url = get_vobiz_public_url()

    websocket_url = public_url.replace(
        "https://",
        "wss://",
        1,
    ).replace(
        "http://",
        "ws://",
        1,
    )

    websocket_url = f"{websocket_url}/voice/ws?phone={phone}"

    return f"""<?xml version="1.0" encoding="UTF-8"?>
            <Response>
                <Stream
                    bidirectional="true"
                    keepCallAlive="true"
                    contentType="audio/x-mulaw;rate=8000">
                    {escape(websocket_url)}
                </Stream>
            </Response>
            """


async def create_vobiz_transport(
    websocket: WebSocket,
) -> FastAPIWebsocketTransport:
    """
    Wait for Vobiz's start event, negotiate the audio format,
    create the Vobiz serializer, and return the Pipecat transport.
    """

    auth_id = settings.vobiz_auth_id
    auth_token = settings.vobiz_auth_token

    if not auth_id:
        raise RuntimeError("VOBIZ_AUTH_ID is not configured.")

    if not auth_token:
        raise RuntimeError("VOBIZ_AUTH_TOKEN is not configured.")

    # Vobiz sends the start event immediately after opening
    # the WebSocket. This gives us:
    #
    # - stream_id
    # - call_id
    # - encoding
    # - sample_rate
    #
    parsed = await parse_vobiz_start(websocket)

    
    stream_id = parsed["stream_id"]
    call_id = parsed["call_id"]

    encoding = parsed["encoding"] or "audio/x-mulaw"
    sample_rate = parsed["sample_rate"] or 8000

    print(
        f"Vobiz stream started: "
        f"call_id={call_id}, "
        f"stream_id={stream_id}, "
        f"encoding={encoding}, "
        f"sample_rate={sample_rate}"
    )

    serializer = VobizFrameSerializer(
        stream_id=stream_id,
        call_id=call_id,
        auth_id=auth_id,
        auth_token=auth_token,
        params=VobizFrameSerializer.InputParams(
            encoding=encoding,
            vobiz_sample_rate=sample_rate,
        ),
    )

    transport = FastAPIWebsocketTransport(
        websocket=websocket,
        params=FastAPIWebsocketParams(
            audio_in_enabled=True,
            audio_out_enabled=True,
            add_wav_header=False,
            serializer=serializer,
        ),
    )

    return transport