from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from datetime import datetime
from .filters import PostFilter
from .forms import ArticlesForm, NewsForm
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
# Create your views here.

class PostList(ListView):
    model = Post
    ordering = 'date_time_create'
    template_name = 'news_portal/news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_sale'] = "Количество свежих новостей:"
        return context


class PostSearch(PostList):
    template_name = 'news_portal/search_post.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'news_portal/new.html'
    context_object_name = 'new'


class ArticlesCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('News_Portal.add_Post',)
    # Указываем нашу разработанную форму
    form_class = ArticlesForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'news_portal/post_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['choice_post'] = 'Создать статью'

        return context

class NewsCreate(ArticlesCreate):
    # Переопределяем форму для новостей
    form_class = NewsForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['choice_post'] = 'Создать новость'  # Изменяем текст на "Создать новость"
        return context


class ArticlesUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('News_Portal.change_Post',)
    form_class = ArticlesForm
    model = Post
    template_name = 'news_portal/post_edit.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()  # Получаем объект
        # Проверяем, является ли поле field_choice равным 0 (статья)
        if self.object.field_choice == 1:
            error_message = 'Вы пытаетесь редактировать новость, а не статью.'
            return redirect(reverse('error_view', kwargs={'error_name': 'Ошибка редактирования', 'error_message': error_message}))

        return super().dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        context['choice_post'] = 'Редактировать статью'  # Изменяем текст на "Создать новость"
        return context

class NewsUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('News_Portal.change_Post',)
    model = Post
    template_name = 'news_portal/post_edit.html'
    form_class = NewsForm

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()  # Получаем объект
        # Проверяем, является ли поле field_choice равным 1 (новость)
        if self.object.field_choice == 0:
            error_message = 'Вы пытаетесь редактировать статью, а не новость.'
            return redirect(reverse('error_view', kwargs={'error_name': 'Ошибка редактирования', 'error_message': error_message}))

        return super().dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['choice_post'] = 'Редактировать новость'  # Изменяем текст на "Создать новость"
        return context


def error_view(request, error_name, error_message):
    return render(request, 'news_portal/error.html', {
        'error_name': error_name,
        'error_message': error_message
    })


class NewsDelete(DeleteView):
    model = Post
    template_name = 'news_portal/post_delete.html'
    success_url = reverse_lazy('post_search')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()  # Получаем объект
        # Проверяем, является ли поле field_choice равным 1 (новость)
        if self.object.field_choice == 0:
            error_message = 'Вы пытаетесь удалить статью, а не новость.'
            return redirect(reverse('error_view', kwargs={'error_message': error_message, 'error_name': 'Ошибка удаления',}))

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['choice_post'] = 'Удаляем новость'
        return context


class ArticlesDelete(DeleteView):
    model = Post
    template_name = 'news_portal/post_delete.html'
    success_url = reverse_lazy('post_search')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()  # Получаем объект
        # Проверяем, является ли поле field_choice равным 1 (новость)
        if self.object.field_choice == 1:
            error_message = 'Вы пытаетесь удалить новость, а не статью.'
            return redirect(reverse('error_view', kwargs={'error_name': 'Ошибка удаления', 'error_message': error_message}))

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['choice_post'] = 'Удаляем статью'
        return context


