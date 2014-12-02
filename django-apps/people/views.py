# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Person, Interaction

def index(request):
    return render(request, 'people/index.html')

def list_people(request):
    people = Person.objects.order_by('name')
    return render(request, 'people/list_people.html', { 'people': people })

def list_interactions(request):
    interactions = Interaction.objects.order_by('-date')
    return render(request, 'people/list_interactions.html',
                  { 'interactions': interactions })

def person(request, person_id):
    person = get_object_or_404(Person, pk=person_id)
    interactions = Interaction.objects.filter(person__id=person.id).order_by("-date")
    return render(request, 'people/person.html', 
                  { 'person': person, 'interactions': interactions })

def interaction(request, interaction_id):
    interaction = get_object_or_404(Interaction, pk=interaction_id)
    return render(request, 'people/interaction.html', { 'interaction': interaction })
