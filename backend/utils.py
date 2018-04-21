from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
import datetime

class HelperClass:

    def get_paginator(qs, page_size, page, paginated_type, **kwargs):
        p = Paginator(qs, page_size)
        try:
            page_obj = p.page(page)
        except PageNotAnInteger:
            page_obj = p.page(1)
        except EmptyPage:
            page_obj = p.page(p.num_pages)
        return paginated_type(
            page=page_obj.number,
            pages=p.num_pages,
            has_next=page_obj.has_next(),
            has_prev=page_obj.has_previous(),
            objects=page_obj.object_list,
            **kwargs
        )

    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        elif request.META.get('HTTP_X_REAL_IP'):
            ip = request.META.get('HTTP_X_REAL_IP')
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    @staticmethod
    def get_si_date(date):
        """
        :param date: datetime object
        :return:
        """
        return datetime.datetime.strptime(date, '%d.%m.%Y')

    @staticmethod
    def to_si_date(date):
        """
        :param date: datetime object
        :return:
        """
        return datetime.datetime.strftime(date, '%d.%m.%Y')