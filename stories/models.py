from urllib.parse import urlparse	# importiram funkciju s kojom uzimam dio url-a
from django.db import models
from django.contrib.auth.models import User	# importiram model u kojem je definirano sve o useru
	
class Story(models.Model):
	title = models.CharField(max_length=200)
	url = models.URLField()
	points = models.IntegerField(default=1)
	moderator = models.ForeignKey(User, related_name='moderated_stories')
	voters = models.ManyToManyField(User, related_name='liked_stories')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	@property				# readonly property
	def domain(self):
		return urlparse(self.url).netloc	# .netloc vraća ime domene

	def __str__(self):
		return self.title	# definiramo normalno ime Story-a

	class Meta:
		verbose_name_plural = 'stories'
