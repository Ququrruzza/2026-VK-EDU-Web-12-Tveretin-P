from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme


def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get("page", 1)

    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        if int(page_number) < 1:
            page = paginator.page(1)
        else:
            page = paginator.page(paginator.num_pages)

    page.elided_page_range = paginator.get_elided_page_range(
        page.number, on_each_side=2, on_ends=1
    )
    return page

def get_next_url(request, default="index"):
    next_url = request.GET.get("next")
    # не даём редиректить на чужие сайты (open redirect)
    if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
        return next_url
    return reverse(default)
