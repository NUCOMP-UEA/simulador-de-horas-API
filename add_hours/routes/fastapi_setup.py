from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from add_hours.routes.activity_router import router_activity
from add_hours.routes.activity_type_router import router_activity_type
from add_hours.routes.student_router import router_student

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router_activity)
app.include_router(router_activity_type)
app.include_router(router_student)

app.mount(
    "/static/assets",
    StaticFiles(directory="add_hours/routes/assets"),
    name="assets",
)
app.mount(
    "/static/styles",
    StaticFiles(directory="add_hours/routes/styles"),
    name="styles",
)


# @app.get("/docs", include_in_schema=False)
# async def custom_swagger_ui_html():
#     return get_swagger_ui_html(
#         openapi_url=app.openapi_url,
#         oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
#         title="Horas SIM",
#         swagger_css_url="/static/styles/swagger_ui.css",
#     )


# @app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
# async def swagger_ui_redirect():
#     return get_swagger_ui_oauth2_redirect_html()


@app.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url="/docs")


# @app.exception_handler(HTTPException)
# async def error_parser(request: Request, exc: HTTPException):
#     return JSONResponse(
#         status_code=exc.status_code,
#         content=dict(code=exc.code, message=exc.message),
#     )
