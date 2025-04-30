from fastapi import APIRouter, Request
from services.nlpAnalysisService import analysis

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# 캐싱을 위한 변수
cached_result = None

# router 생성
router = APIRouter(prefix="/analysis", tags=["analysis"])
# 템플릿 설정 
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def sentiment_analysis(request: Request):
    global cached_result
    
    # 결과가 캐시되어 있지 않은 경우에만 분석 실행
    if cached_result is None:
        cached_result = analysis()
    
    # HTML 템플릿에 결과 전달
    return templates.TemplateResponse(
        request=request,
        name="analysis_nlp.html", 
        context={
            "request": request, 
            "data": cached_result
        }
    )