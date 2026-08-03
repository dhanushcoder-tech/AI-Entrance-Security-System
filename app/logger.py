from datetime import datetime

last_seen = {}

def can_log(student_id):

    now = datetime.now()

    if student_id not in last_seen:
        last_seen[student_id] = now
        return True

    elapsed = (now - last_seen[student_id]).total_seconds()

    if elapsed >= 30:
        last_seen[student_id] = now
        return True

    return False