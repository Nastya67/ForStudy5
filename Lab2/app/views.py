from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from app import database


def index(request):
    db = database.Database()
    context = {"db": db.selectGames()}
    if request.method == 'POST':
        if request.POST.get('Update'):
            url = reverse('update', kwargs={'arg': request.POST['Update'].replace(', ', 'and')})
            response = HttpResponseRedirect(url)
            return response
        if request.POST.get('InsertGame'):
            return HttpResponseRedirect(reverse('insertGame'))
        if request.POST.get('InsertTime'):
            return HttpResponseRedirect(reverse('insertTime'))
        if request.POST.get('Load'):
            db.load()
        if request.POST.get('Delete'):
            idGame, Time = request.POST['Delete'].split(', ')
            db.delRow(idGame, Time)
        if request.POST.get("SearchJudge"):
            d= {0:"Woman", 1:"Man"}
            context = {"db":db.selectGamesWhereJ(request.POST['Judge']),
                       "search":"Judge: "+d[int(request.POST['Judge'])]}
        if request.POST.get("SearchDate"):
            context = {"db":db.selectGamesWhereD(request.POST['date0'].replace("T", " "),
                                                 request.POST['date1'].replace("T", " ")),
                       "search":"Date: "+request.POST['date0'].replace("T", " ")+" - "+request.POST['date1'].replace("T", " ")}
    template = loader.get_template('index.html')
    db.conClose()
    return HttpResponse(template.render(context, request))

def insertGame(request):
    db = database.Database()
    if request.method == 'POST':
        game = {'idGame':request.POST['idGame'],
                'Score': ":".join([request.POST['score0'], request.POST['score1']]),
                'Date': request.POST['date'].replace('T', ' '),
                'Comments': request.POST['comment'],
                'Winner':request.POST['winner'],
                'Loser':request.POST['loser'],
                'Judge':request.POST['judge'],
                'Address':request.POST['address'],
                'Time':request.POST['time']}
        res = db.insertGame(game)
        db.conClose()
        if res != 'OK':
            template = loader.get_template('Error.html')
            context = {"error":res}
            return HttpResponse(template.render(context, request))
        return HttpResponseRedirect(reverse('index'))
    template = loader.get_template('insertGame.html')
    context = {'vars':{'Commands': db.selectCommands(),
                       'Judges': db.selectJudges(),
                       'Address': db.selectAddress()}}
    db.conClose()
    return HttpResponse(template.render(context, request))

def insertTime(request):
    db = database.Database()
    if request.method == 'POST':
        game = {'idGame':request.POST['idGame'],
                'Score': ":".join([request.POST['score0'], request.POST['score1']]),
                'Winner':request.POST['winner'],
                'Time':request.POST['time']}
        res = db.insertTime(game)
        db.conClose()
        if res != 'OK':
            template = loader.get_template('Error.html')
            context = {"error":res}
            return HttpResponse(template.render(context, request))
        return HttpResponseRedirect(reverse('index'))
    template = loader.get_template('insertTime.html')
    context = {'vars':{'Commands': db.selectCommands(),
                       'Judges': db.selectJudges(),
                       'Address': db.selectAddress()}}
    db.conClose()
    return HttpResponse(template.render(context, request))


def update(request, arg):
    db = database.Database()
    idGame, Time = arg.split('and')
    date, comment = db.selectDateWhere(idGame)
    context = {'game':{"idGame":idGame,'Time':Time, 'Date': str(date)[:-3].replace(' ', 'T'),
                       'Score': db.selectScoreWhere(idGame, Time).split(':'),
                       'Comments':comment,
                       'Winner':db.selectWinner(idGame, Time), 'Loser':db.selectLoser(idGame, Time),
                       'Judge': db.selectJudgeWhere(idGame),
                       'Address':db.selectAddressWhere(idGame)}}
    if request.method == 'POST':
        if request.POST['date'] != context['game']['Date']:
            db.updateDate(idGame, request.POST['date'].replace('T', ' '))
        if [request.POST['score0'], request.POST['score1']] != context['game']['Score']:
            db.updateScore(idGame, Time, ":".join([request.POST['score0'],  request.POST['score1']]))
        if request.POST['comment'] != context['game']['Comments']:
            db.updateComment(idGame, request.POST['comment'])
        if request.POST['winner'] != context['game']['Winner']:
            db.updateWinner(idGame, Time, request.POST['winner'])
        if request.POST['judge'] != context['game']['Judge']:
            db.updateJudge(idGame, request.POST['judge'])
        if request.POST['address'] != context['game']['Address']:
            db.updateAddress(idGame, request.POST['address'])
        db.conClose()
        return HttpResponseRedirect(reverse('index'))
    context['vars'] = {'Commands':db.selectCommands(),
                       'Judges': db.selectJudges(),
                       'Address': db.selectAddress()}
    db.conClose()
    template = loader.get_template('update.html')
    return HttpResponse(template.render(context, request))

# Create your views here.
