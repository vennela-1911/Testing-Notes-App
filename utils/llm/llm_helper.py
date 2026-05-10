import time


def generate_note_data():

    timestamp = int(time.time())

    return {
        "title": f"AI Note {timestamp}",
        "description": (
            f"AI Generated Description "
            f"{timestamp}"
        )
    }