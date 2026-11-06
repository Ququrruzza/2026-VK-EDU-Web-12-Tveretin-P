from .mock_data import BEST_MEMBERS, POPULAR_TAGS


def sidebar(request):
    return {
        "popular_tags": POPULAR_TAGS,
        "best_members": BEST_MEMBERS,
    }