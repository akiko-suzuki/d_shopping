import re

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def paginate_query(request, queryset):
    """ ページネーション """

    current_page = 1
    query_string = ""

    if request.GET:
        query_string = request.GET.urlencode()
        query_string = re.sub(r'page=\d+&?', '', query_string)

        current_page = request.GET.get('page')

    paginator = Paginator(queryset, 2)
    try:
        page_obj = paginator.page(current_page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    page_obj.query_string = query_string

    return page_obj
