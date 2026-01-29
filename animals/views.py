from django.shortcuts import render, redirect, get_object_or_404
from .models import Animal, AnimalHistory, MedicalVisit, MedicalDocument
from .forms import AnimalForm, MedicalVisitForm, MedicalDocumentForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Favorite




def is_employee(user):
    return user.groups.filter(name__in=[
        'Administrator systemu',
        'Pracownik schroniska',
        'Kierownik schroniska'
    ]).exists()


def is_vet(user):
    return user.groups.filter(name='Weterynarz').exists()


def is_admin(user):
    return user.groups.filter(name='Administrator systemu').exists()



def animal_list(request):
    animals = Animal.objects.all()

    # --- FILTRY ---
    wiek = request.GET.get('wiek')
    rasa = request.GET.get('rasa')

    if wiek:
        animals = animals.filter(wiek=wiek)

    if rasa:
        animals = animals.filter(rasa__icontains=rasa)

    # do listy ras (unikalne)
    rasy = Animal.objects.values_list('rasa', flat=True).distinct()

    context = {
        'animals': animals,
        'rasy': rasy,
        'selected_wiek': wiek,
        'selected_rasa': rasa,
    }
    return render(request, 'animals/animal_list.html', context)



@login_required
@permission_required('animals.add_animal', raise_exception=True)
def animal_create(request):
    if request.method == 'POST':
        form = AnimalForm(request.POST, request.FILES)
        if form.is_valid():
            # zapisujemy zwierzaka
            animal = form.save()

            # słownik: kod statusu -> ładna etykieta ("Do adopcji" itd.)
            status_labels = dict(Animal.STATUS_CHOICES)
            current_status_label = status_labels.get(animal.status, animal.status)

            # dodajemy wpis w historii: przyjęcie do schroniska
            AnimalHistory.objects.create(
                animal=animal,
                action="Przyjęcie do schroniska",
                new_status=current_status_label,
            )

            return redirect('animal_list')
    else:
        form = AnimalForm()

    return render(request, 'animals/animal_form.html', {
        'form': form,
        'mode': 'create',
    })

@login_required
@permission_required('animals.change_animal', raise_exception=True)
def animal_update(request, pk):
    animal = get_object_or_404(Animal, pk=pk)

    # zapamiętujemy stary status PRZED zmianą
    old_status_code = animal.status

    if request.method == 'POST':
        form = AnimalForm(request.POST, request.FILES, instance=animal)
        if form.is_valid():
            # zapisujemy zmiany
            updated_animal = form.save()

            new_status_code = updated_animal.status

            # jeżeli status się zmienił, dopisujemy wpis do historii
            if old_status_code != new_status_code:
                status_labels = dict(Animal.STATUS_CHOICES)
                old_label = status_labels.get(old_status_code, old_status_code)
                new_label = status_labels.get(new_status_code, new_status_code)

                AnimalHistory.objects.create(
                    animal=updated_animal,
                    action=f"Zmiana statusu z '{old_label}' na '{new_label}'",
                    old_status=old_label,
                    new_status=new_label,
                )

            return redirect('animal_list')
    else:
        form = AnimalForm(instance=animal)

    return render(request, 'animals/animal_form.html', {
        'form': form,
        'mode': 'edit',
        'animal': animal,
    })


def animal_detail(request, pk):
    """
    Szczegóły pojedynczego zwierzaka + jego historia.
    """
    animal = get_object_or_404(Animal, pk=pk)
    history = animal.history.all()  # thanks to related_name='history' w modelu AnimalHistory

    return render(request, 'animals/animal_detail.html', {
        'animal': animal,
        'history': history,
    })

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect

@login_required
@user_passes_test(lambda u: u.groups.filter(name="Opiekun zwierząt").exists())
def assign_to_me(request, pk):
    animal = get_object_or_404(Animal, pk=pk)

    # jeśli już ma opiekuna – nie pozwalamy
    if animal.opiekun is None:
        animal.opiekun = request.user
        animal.save()

    return redirect('animal_detail', pk=pk)

@login_required
@user_passes_test(lambda u: is_vet(u) or is_admin(u))
def medical_visit_create(request, pk):
    """
    Dodanie wizyty medycznej dla konkretnego zwierzaka.
    """
    animal = get_object_or_404(Animal, pk=pk)

    if request.method == 'POST':
        form = MedicalVisitForm(request.POST)
        if form.is_valid():
            visit = form.save(commit=False)
            visit.animal = animal
            visit.save()

            # (opcjonalnie) dopis do historii zwierzęcia:
            AnimalHistory.objects.create(
                animal=animal,
                action=f"Wizyta medyczna: {visit.visit_date}",
            )

            return redirect('animal_detail', pk=animal.pk)
    else:
        form = MedicalVisitForm()

    return render(request, 'animals/medical_visit_form.html', {
        'form': form,
        'animal': animal,
    })

@login_required
@permission_required('animals.view_medicaldocument', raise_exception=True)
def medical_documents_list(request, pk):
    animal = get_object_or_404(Animal, pk=pk)
    documents = animal.medical_documents.all()
    return render(request, 'animals/medical_documents_list.html', {
        'animal': animal,
        'documents': documents,
    })

@login_required
@permission_required('animals.add_medicaldocument', raise_exception=True)
def medical_document_add(request, pk):
    animal = get_object_or_404(Animal, pk=pk)

    if request.method == 'POST':
        form = MedicalDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.animal = animal
            doc.save()

            # (opcjonalnie) wpis do historii
            AnimalHistory.objects.create(
                animal=animal,
                action=f"Dodano dokument medyczny: {doc.title}",
            )

            return redirect('medical_documents_list', pk=animal.pk)
    else:
        form = MedicalDocumentForm()

    return render(request, 'animals/medical_document_form.html', {
        'animal': animal,
        'form': form,
    })

def favorites_list(request):
    """
    Lista ulubionych:
    - zalogowany: z bazy
    - niezalogowany: z session
    """
    if request.user.is_authenticated:
        favorites = Favorite.objects.filter(user=request.user).select_related("animal")
        animals = [f.animal for f in favorites]
    else:
        fav_ids = request.session.get("favorite_animal_ids", [])
        animals = Animal.objects.filter(pk__in=fav_ids)

    return render(request, "animals/favorites_list.html", {"animals": animals})


def toggle_favorite(request, pk):
    """
    Dodaj/usuń z ulubionych.
    """
    animal = get_object_or_404(Animal, pk=pk)

    next_url = request.GET.get("next") or reverse("animal_list")

    # --- zalogowany -> DB ---
    if request.user.is_authenticated:
        fav, created = Favorite.objects.get_or_create(user=request.user, animal=animal)
        if not created:
            fav.delete()
        return redirect(next_url)

    # --- niezalogowany -> session ---
    fav_ids = request.session.get("favorite_animal_ids", [])
    if pk in fav_ids:
        fav_ids.remove(pk)
    else:
        fav_ids.append(pk)
    request.session["favorite_animal_ids"] = fav_ids
    request.session.modified = True

    return redirect(next_url)


def about_shelter(request):
    """
    Strona informacyjna: lokalizacja schroniska i godziny otwarcia.
    """
    return render(request, 'animals/about.html')

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Opiekun zwierząt').exists())
def my_animals(request):
    animals = Animal.objects.filter(opiekun=request.user)
    return render(request, 'animals/my_animals.html', {
        'animals': animals
    })
