from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from app import database


def index(request):
    db = database.Database()
    if request.method == 'POST':
        if request.POST.get('Delete'):
            idGame, Time = request.POST['Delete'].split(', ')
            db.delRow(idGame, Time)
        if request.POST.get('Update'):
            url = reverse('update', kwargs={'arg': '1and1'})
            response = HttpResponseRedirect(url)
            return response
    template = loader.get_template('index.html')
    context = {"show":True, "db": db.selectGames()}
    context["range"] = range(len(context["db"]))
    return HttpResponse(template.render(context, request))

def update(request, arg):
    template = loader.get_template('update.html')
    context = {"show": True, 'arg':arg, 'game':{'Date':'1.01.01'}, 'dateVars':['11', '12', '13']}
    return HttpResponse(template.render(context, request))

# Create your views here.
