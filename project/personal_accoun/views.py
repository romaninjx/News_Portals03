from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from News_Portal.models import Author
from django.contrib.auth.models import Group


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'personal_accoun/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='Author').exists()
        return context


@login_required
def upgrade_me(request):

    user = request.user
    print(user)
    author_group = Group.objects.get(name='Author')
    if not request.user.groups.filter(name='Author').exists():
        author_group.user_set.add(user)
        Author.objects.create(author=user)
    return redirect('/accoun/user_lk/')
