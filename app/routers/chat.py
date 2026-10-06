from fastapi import APIRouter
from app.models.schemas import ApiResponse, ChatRequest, ChatResponseData
from app.services.gemini_chat import answer_farming_question

router = APIRouter(prefix="/api/v1/ai", tags=["AI Farming Assistant (Chatbot)"])

@router.post("/chat", response_model=ApiResponse[ChatResponseData])
async def endpoint_chat_assistant(request: ChatRequest):
    """
    Endpoint Chatbot Asisten Urban Farming via Gemini API.
    Memberikan konsultasi ramah & praktis terkait kendala tanaman secara kontekstual.
    """
    response_data = await answer_farming_question(
        message=request.message,
        tanaman_aktif=request.tanaman_aktif,
        history=request.history
    )

    return ApiResponse(
        success=True,
        data=response_data,
        message="Respon asisten AI berhasil dihasilkan"
    )
