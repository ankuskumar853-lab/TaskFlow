import re


def parse_task(description: str):

    original_text = description
    text = description.lower()

    # -------------------
    # Priority
    # -------------------

    if (
        "urgent" in text or
        "asap" in text or
        "high priority" in text or
        "high" in text
    ):
        priority = "high"

    elif (
        "low priority" in text or
        "low" in text or
        "whenever" in text
    ):
        priority = "low"

    elif (
        "medium priority" in text or
        "medium" in text
    ):
        priority = "medium"

    else:
        priority = "medium"




    # -------------------
    # Due Date
    # -------------------

    due_date = None

    keywords = [
        "today",
        "tomorrow",
        "next monday",
        "next tuesday",
        "next wednesday",
        "next thursday",
        "next friday",
        "next saturday",
        "next sunday",
        "next week",
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday"
    ]

    for word in keywords:

        if word in text:
            due_date = word
            break

    # -------------------
    # Title
    # -------------------

    title = original_text

    remove_words = [
        "urgent",
        "asap",
        "whenever",
        "high",
        "medium",
        "low",
        "high priority",
        "medium priority",
        "low priority"
    ]

    if due_date:
        remove_words.append(due_date)

    for word in remove_words:

        title = re.sub(
            word,
            "",
            title,
            flags=re.IGNORECASE
        )

    title = title.strip()

    if title == "":
        title = "Untitled task"

    return {
        "title": title,
        "priority": priority,
        "due_date": due_date
    }