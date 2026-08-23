from ai_core.intent import Intent


INTENT_KEYWORDS: tuple[tuple[Intent, tuple[str, ...]], ...] = (
    (
        Intent.RESCHEDULE,
        (
            "reschedule",
            "change my booking",
            "change my appointment",
            "إعادة جدولة",
            "غير موعد",
            "غيّر موعد",
        ),
    ),
    (
        Intent.CANCEL,
        (
            "cancel",
            "cancel my booking",
            "cancel my appointment",
            "إلغاء",
            "الغي",
            "ألغي",
        ),
    ),
    (
        Intent.CHECK_AVAILABILITY,
        (
            "availability",
            "available",
            "available slots",
            "متاح",
            "المواعيد المتاحة",
            "الأوقات المتاحة",
        ),
    ),
    (
        Intent.GET_SERVICES,
        (
            "services",
            "what services",
            "الخدمات",
            "ما هي الخدمات",
            "وش الخدمات",
        ),
    ),
    (
        Intent.GET_STAFF,
        (
            "staff",
            "employees",
            "who works",
            "الموظفين",
            "الموظفات",
            "الطاقم",
        ),
    ),
    (
        Intent.BOOK,
        (
            "book",
            "book an appointment",
            "make a booking",
            "احجز",
            "حجز موعد",
            "أبغى أحجز",
            "اريد احجز",
            "أريد أحجز",
        ),
    ),
)


def detect_intent(message: str) -> Intent:
    """Detect a supported intent from a user message using deterministic rules."""

    normalized_message = message.strip().lower()

    if not normalized_message:
        return Intent.UNKNOWN

    for intent, keywords in INTENT_KEYWORDS:
        if any(keyword in normalized_message for keyword in keywords):
            return intent

    return Intent.UNKNOWN
