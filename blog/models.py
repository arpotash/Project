from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=255) # заголовок поста
    content = models.TextField(max_length=10000) # текст поста
    author = models.ForeignKey(User)
    likes = models.IntegerField(default=0)
    #slug = models.CharField(verbose_name='Транслит', max_length=200, blank=True)
    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/blog/%i/" % self.id
class Comment(models.Model):
	post = models.ForeignKey(Post, related_name='comments')
	name = models.ForeignKey(User)
	email = models.EmailField()
	body = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	active = models.BooleanField(default=True)

	class Meta:
		ordering = ('created',)

	def __str__(self):
		return 'Comment by {} on {}'.format(self.name, self.post)

