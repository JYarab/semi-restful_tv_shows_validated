from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from .models import Show

# index redirect to show list
def index(request):
    return redirect('/shows')

# render shows list page
def shows(request):
    context = {
        'shows' : Show.objects.all()
    }
    return render(request, 'shows.html', context)

# render add show page
def show_new(request):
    return render(request, 'add_show.html')

# validate input for new show and create if no errors
def show_create(request):
    # input validation and error message logging redirect back if errors
    errors = Show.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/shows/new')
    # no errors create new show in DB
    else:
        new_show = Show.objects.create(title=request.POST['title'], network=request.POST['network'], release_date=request.POST['date'], description=request.POST['desc'])    
        return redirect(f'/shows/{new_show.id}')

#render show info page
def show_info(request, id):
    context = {
        "show" : Show.objects.get(id=id)
    }
    return render(request, 'show_info.html', context)

#render edit page
def show_edit(request, id):
    context = {
        "show" : Show.objects.get(id=id)
    }
    return render(request, 'edit_show.html', context)

# validate input for show update and update DB if no errors
def show_update(request, id):
    # input validation and error message logging redirect back if errors    
    errors = Show.objects.basic_validator(request.POST)
    #check for and remove non-unique title errors
    if 'unique' in errors['title']:
        del errors['title']
    #check for remaining errors log and redirect back to edit page 
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/shows/{id}/edit')
    # no errors update show in DB
    else:
        Show.objects.filter(id=id).update(title=request.POST['title'], network=request.POST['network'], release_date=request.POST['date'], description=request.POST['desc'])
        show = Show.objects.get(id=id)
        show.save()
        return redirect(f'/shows/{id}')

#delete show from DB
def show_destroy(request, id):
    Show.objects.filter(id=id).delete()
    return redirect('/shows')