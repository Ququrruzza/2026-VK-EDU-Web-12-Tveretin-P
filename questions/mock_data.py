from core.mock_data import CURRENT_USER, USERS

TAGS = ["python", "django", "MySQL", "perl", "TechnoPark", "bender", "black-jack", "css", "Firefox"]
VOTES = ["up", None, "down"]
TIMES = ["15 minutes ago", "2 hours ago", "yesterday", "3 days ago", "last week"]

QUESTIONS = []
for i in range(1, 121):
    QUESTIONS.append({
        "id": i,
        "title": f"Question title {i}",
        "text": (
            f"Text of question {i}. I have been trying to solve this for a while, "
            "read the docs and searched everywhere, but nothing helps. "
            "Maybe someone here has already faced the same problem?"
        ),
        "author": USERS[i % len(USERS)],
        "tags": [TAGS[i % len(TAGS)], TAGS[(i + 4) % len(TAGS)]],
        "rating": (i * 7) % 25 - 5,
        "vote": VOTES[i % len(VOTES)],
        "answers_count": (i * 7) % 31,
        "created": TIMES[i % len(TIMES)],
    })


def get_answers(question):
    answers = []
    for j in range(1, question["answers_count"] + 1):
        answers.append({
            "id": j,
            "text": f"Answer {j} to question {question['id']}. Try to restart everything and read the error message carefully.",
            "author": CURRENT_USER if j % 4 == 0 else USERS[j % len(USERS)],
            "rating": (j * 5) % 13 - 3,
            "vote": VOTES[j % len(VOTES)],
            "is_correct": j == 1,
            "created": TIMES[j % len(TIMES)],
        })
    return answers