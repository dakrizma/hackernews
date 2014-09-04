import datetime
import heapq		# sort algoritam
from stories.models import Story
from stories.forms import StoryForm
from django.utils.timezone import utc
from django.shortcuts import  render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
# from django.http import HttpResponse	 
#from django.template import loader, Context		# html

def score(story, gravity=1.8, timebase=120):
	points = (story.points - 1)**0.8
	now = datetime.datetime.utcnow().replace(tzinfo=utc)		# django radi sa utc, pa...
	age = int((now - story.created_at).total_seconds())/60		# default će vratiti float, pa zato int

	return points/(age+timebase)**1.8

def top_stories(top=180, consider=1000):
	latest_stories = Story.objects.all().order_by('-created_at')[:consider]		# ovo zadnje znači od 0-1000
	return heapq.nlargest(top, latest_stories, key=score)
	# ranked_stories = sorted([(score(story), story) for story in latest_stories], reverse=True)	# rankiramo story od boljem prema lošijem
	# return [story for _, story in ranked_stories][:top]			# vraćamo najveći rank broj

def index(request):
	stories = top_stories(top=30)
	if request.user.is_authenticated():
		liked_stories = request.user.liked_stories.filter(id__in=[story.id for story in stories])	# id__in provjerava da li postoji ijedan id
	else:
		liked_stories = []
	# template = loader.get_template('stories/index.html')
	# context = Context({'stories': stories})			# definiramo koje lokalne varijable ćemo koristiti
	# response = template.render(context)
	# return HttpResponse(response)
	return render(request, 'stories/index.html', {
		'stories': stories,
		'user': request.user,
		'liked_stories': liked_stories
	})

@login_required
def story(request):
	if request.method == 'POST':				# ako forma nije prazna
	 	form = StoryForm(request.POST)
	 	if form.is_valid():						# ako forma nije cijela ispunjena
	 		story = form.save(commit=False)		# snimi u "clipboard", ali nemoj još snimiti
	 		story.moderator = request.user		# ovo radimo zato što moderator je NOT_NULL
	 		story.save()						# snimi
	 		return HttpResponseRedirect('/')	# vrati na početnu stranicu
	else:
		form = StoryForm()						# forma je prazna

	return render(request, 'stories/story.html', {'form': form})

@login_required
def vote(request):
	story = get_object_or_404(Story, pk=request.POST.get('story'))
	story.points += 1
	story.save()
	user = request.user
	user.liked_stories.add(story)		# vežemo usera i story za koje je glasovao
	user.save()							# , tako da ne može opet glasati
	return HttpResponse()