from django import forms
from .models import Post, Category
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

class ArticlesForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        label='Категории'
    )

    class Meta:
        model = Post
        fields = ['name_post', 'text_post', 'categories', 'post_link']

    def __init__(self, *args, **kwargs):
        super(ArticlesForm, self).__init__(*args, **kwargs)
        self.fields['categories'].label_from_instance = lambda obj: obj.name_category
        self.fields['post_link'].label_from_instance = lambda obj: obj.author

    def save(self, commit=True):
        post = super().save(commit=False)
        if commit:
            post.save()
            self.save_m2m()  # Сначала сохраняем  объект, потом устанавливаем многие ко многим
        return post

class NewsForm(ArticlesForm):
    class Meta(ArticlesForm.Meta):
        fields = ArticlesForm.Meta.fields  # Сохраняем все поля из ArticlesForm

    def save(self, commit=True):
        post = super().save(commit=False)
        post.field_choice = 1  # Устанавливаем поле field_choice для новостей
        if commit:
            post.save()  # Сохраняем объект
            self.save_m2m()  # Затем сохраняем многие ко многим
        return post




class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user
