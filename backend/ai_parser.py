import re


def parse_task(description: str):
    original_text = description
    text = description.lower()

    # ==========================
    # Priority
    # ==========================

    if "urgent" in text or "asap" in text:
        priority = "high"

    elif "whenever" in text or "low priority" in text:
        priority = "low"

    else:
        priority = "medium"

    # ==========================
    # Due Date
    # ==========================

    due_date = None

    date_phrases = [
        "today",
        "tomorrow",
        "next week",
        "next monday",
        "next tuesday",
        "next wednesday",
        "next thursday",
        "next friday",
        "next saturday",
        "next sunday",
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday",
    ]

    for phrase in date_phrases:
        if phrase in text:
            due_date = phrase
            break

    # ==========================
    # Title
    # ==========================

    title = original_text

    # Assignment ke according:
    # priority decide karne wale keyword ke alawa
    # saare priority keywords remove honge.

    priority_words = [
        "urgent",
        "asap",
        "whenever",
        "low priority",
    ]

    for word in priority_words:
        title = re.sub(
            re.escape(word),
            "",
            title,
            flags=re.IGNORECASE
        )

    # Matched due-date phrase ke
    # saare occurrences remove karo.

    if due_date:
        title = re.sub(
            re.escape(due_date),
            "",
            title,
            flags=re.IGNORECASE
        )

    title = title.strip()

    if not title:
        title = "Untitled task"

    return {
        "title": title,
        "priority": priority,
        "due_date": due_date
    }