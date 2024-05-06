from django.shortcuts import render
from django.db.models import Q

from mthapp.models import Post


# Create your views here.
def SearchResult(request):
    movies=None
    query=None
    if 'q' in request.GET:
        query=request.GET.get('q')
        movies=Post.objects.all().filter(Q(moviename__contains=query) | Q(category__name__icontains=query))
        return render(request,'search.html',{'query':query,'movies':movies})