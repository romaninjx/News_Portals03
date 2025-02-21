from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    user_rating = models.IntegerField(default=0)

    def update_rating(self)->None:
        posts = Post.objects.filter(post_link=self)
        posts_rating = sum(post.rating_post_user * 3 for post in posts)
        comments_rating = sum(comment.rating for comment in Comment.objects.filter(user=self.author))
        rating_of_comments_on_users_post = sum(comment.rating for post in posts for comment in Comment.objects.filter(post=post))
        self.user_rating = posts_rating + rating_of_comments_on_users_post + comments_rating
        self.save()

class Category(models.Model):
    name_category = models.CharField(max_length=30, unique=True)


POSTS_CHOIСES = [(0 ,"Статья"), (1, "Новость")]

class Post(models.Model):
    post_link = models.ForeignKey(Author, on_delete=models.CASCADE)
    field_choice = models.BooleanField(default=0, choices=POSTS_CHOIСES)   # 0 - статья \ 1 - новость
    date_time_create = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    name_post = models.TextField()
    text_post = models.TextField()
    rating_post_user = models.IntegerField(default=0)   #возможно нужно чтото придумать

    def get_categories(self):
        return self.categories.all()

    def get_post_type_display(self):
        return dict(POSTS_CHOIСES)[self.field_choice]

    def choice_display(self):
        return f'{Post.objects.get(pk=self).get_field_choice_display()}'

    def __str__(self):
        return f'{self.name_post.title()}: {self.text_post[:20]}...'


    def like(self) ->None:
        self.rating_post_user += 1
        self.save()

    def dislike(self) ->None:
        self.rating_post_user -= 1
        self.save()

    def preview(self):
        return f'{self.text_post[:124]}...'

    def comments_print(self):   # вывод всех коментариев
        list_comments = Comment.objects.filter(post=self)
        for comment in list_comments:
            print(f'Коментарии c рейтингом {comment.rating} {comment.user.username}: "{comment.text}", {comment.date_time_add}')

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date_time_add = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self) ->None:
        self.rating += 1
        self.save()


    def dislike(self) ->None:
        self.rating -= 1
        self.save()
