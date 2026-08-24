from database.repositories.services import get_all_services
from database.repositories.staff import get_all_staff


def get_services() -> list[dict]:
    """Return all active services through existing repository logic."""
    return get_all_services()


def get_staff() -> list[dict]:
    """Return all active staff through existing repository logic."""
    return get_all_staff()
