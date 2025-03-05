from django_filters import FilterSet
from .models import Post


class PostFilter(FilterSet):
    class Meta:
        model = Post  # Указываем модель, которую будем фильтровать
        fields = {
            'name_post': ['icontains'],
            'post_link__author__username': ['iexact'],
            'date_time_create': ['date'],
        }
