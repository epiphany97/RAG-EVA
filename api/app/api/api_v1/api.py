from .endpoints import llm_ep,t2t_gen
from fastapi import APIRouter


router = APIRouter()


router.include_router(llm_ep.router,prefix="/llm",tags=["llm"])
router.include_router(t2t_gen.router, prefix="/t2t", tags=["text-to-text"])  # 添加 t2t 路由
