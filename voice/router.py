from fastapi import HTTPException
from fastapi import APIRouter, Request, Response, WebSocket

from pipecat.runner.types import WebSocketRunnerArguments

from agent.bot import bot

from voice.services import build_vobiz_answer_xml


router = APIRouter(tags=["voice"],)


@router.api_route("/answer", methods=["GET", "POST"],)
async def vobiz_answer(request: Request,):
    """
    Vobiz calls this endpoint when an incoming call is answered.

    We return Vobiz XML telling it to open a bidirectional
    WebSocket connection to /voice/ws.
    """
    form = await request.form()

    phone = str(
        form.get("From")
        or form.get("CallerName")
        or ""
    )

    if not phone:
        raise HTTPException(
            status_code=400,
            detail="Caller phone number missing",
        )

    xml = build_vobiz_answer_xml(phone)

    return Response(content=xml, media_type="application/xml",)


@router.websocket("/voice/ws")
async def vobiz_websocket(websocket: WebSocket,):
    """
    Vobiz opens this WebSocket after receiving the XML
    from /answer.

    The WebSocket is passed directly into the Pipecat bot.
    """
    phone = websocket.query_params.get("phone")

    if not phone:
        await websocket.close(code=1008)
        return

    await websocket.accept()

    runner_args = WebSocketRunnerArguments(websocket=websocket, transport_type="vobiz",)

    await bot(runner_args,phone)