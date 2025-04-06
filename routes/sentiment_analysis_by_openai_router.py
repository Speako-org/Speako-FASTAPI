from fastapi import APIRouter, Request
from services import sentiment_analysis_by_openai_svc

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

cached_result = None

# router 생성
router = APIRouter(prefix="/analysis", tags=["analysis"])
# 템플릿 설정 
templates = Jinja2Templates(directory="templates")

# 캐싱을 위한 변수


@router.get("/", response_class=HTMLResponse)
async def sentiment_analysis_by_openai(request: Request):
    global cached_result
    
    # 결과가 캐시되어 있지 않은 경우에만 분석 실행
    if cached_result is None:
        cached_result = sentiment_analysis_by_openai_svc.analyzs_sentiment()
    
    # HTML 템플릿에 결과 전달
    return templates.TemplateResponse(
        request=request,
        name="analysis_result.html", 
        context={
            "request": request, 
            "data": cached_result
            }
    )