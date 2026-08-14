from fastapi import FastAPI

from api.routes.services import router as services_router
from api.routes.bookings import router as bookings_router
from api.routes.customers import router as customers_router

app = FastAPI(
    title="AI Booking Agent API",
    version="0.1.0",
)

app.include_router(bookings_router)
app.include_router(services_router)
app.include_router(customers_router)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "ai-booking-agent",
    }