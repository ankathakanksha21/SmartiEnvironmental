"""Creates the app and adds the routes and error handlers."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app import database, models
from app.routes import customers, jobs, staff


@asynccontextmanager
async def lifespan(app):
    # Create any missing tables, so a new developer has no database setup step.
    models.Base.metadata.create_all(database.engine)
    yield


app = FastAPI(title="Smarti Environmental CRM", lifespan=lifespan)
app.include_router(customers.router)
app.include_router(staff.router)
app.include_router(jobs.router)


@app.exception_handler(RequestValidationError)
def invalid_input(request, exc):
    """Turn validation failures into {field: message} for the frontend forms."""
    errors = {}
    for error in exc.errors():
        field = error["loc"][-1]
        # Pydantic adds this prefix to the messages we write in schemas.py.
        errors[field] = error["msg"].removeprefix("Value error, ")
    return JSONResponse(status_code=422, content={"errors": errors})


@app.exception_handler(OverflowError)
def id_too_large(request, exc):
    """An id too large for SQLite can't belong to any record."""
    return JSONResponse(status_code=404, content={"detail": "Record not found."})


@app.exception_handler(Exception)
def unexpected_error(request, exc):
    """Answer in JSON so the page can show the message. The traceback still goes to the terminal."""
    return JSONResponse(
        status_code=500, content={"detail": "Something went wrong on the server."}
    )
