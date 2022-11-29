from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib import messages


from .forms import (
    UserForm, LoginForm, ProjetForm, UpdateProjetForm,
    SousTacheForm
)
from .models import User, Projet, SousTache

# Create your views here.

def index(request):

    if request.user.is_authenticated:
        user_auth = request.user.email
        return render(request, 'pages/index.html', { 'user': user_auth})
    return render(request, 'pages/index.html')



@login_required
def create_projet_view(request):

    if not request.user.is_authenticated:
        return redirect("apptache:login")

    form = ProjetForm()
    if request.POST:
        form = ProjetForm(request.POST)
        if form.is_valid():
            projet = Projet.objects.create(
                libelle=form.cleaned_data.get('libelle'),
                date_debut=form.cleaned_data.get('date_debut'),
                date_fin=form.cleaned_data.get('date_fin'),
                owner=request.user
            )
            projet.save()
            form = ProjetForm()

            context = { 'form': form, 'projet': projet}
            return render(request, "pages/projet/create_projet.html", context)
    context = { 'form': form }
    return render(request, "pages/projet/create_projet.html", context)
    
@login_required
def projet_list_view(request):

    obj_tache = Projet.objects.filter(owner=request.user)

    return render(request, "pages/projet/liste_projet.html", { "obj_tache": obj_tache })

def delete_tache(request, pk):

    projet = Projet.objects.get(pk=pk)
    projet.delete()
    return redirect("apptache:liste_projet")


def update_projet_view(request, pk):

    projet = Projet.objects.get(pk=pk)
    form =  UpdateProjetForm(instance=projet)

    if request.POST:
        form = UpdateProjetForm(request.POST, instance=projet)
        if form.is_valid():
            form.save()
            return redirect("apptache:liste_projet")
    return render(request, "pages/projet/update_projet.html", { 'form': form })
    

def create_sous_tache_view(request, pk):

    projet = Projet.objects.get(pk=pk)
    form = SousTacheForm()
    print("NOMBRE DE SOUS TACHES: ", SousTache.objects.deviner_etiquette(projet))
    if request.POST:

        form = SousTacheForm(request.POST)
        if form.is_valid():

            sous_tache = SousTache.objects.create(
                etiquette=SousTache.objects.deviner_etiquette(projet),
                couleur="Gris",
                nom_tache=form.cleaned_data.get("nom_tache"),
                executant=form.cleaned_data.get("executant"),
                date_debut=form.cleaned_data.get("date_debut"),
                date_fin=form.cleaned_data.get("date_fin"),
                projet=projet
            )

            sous_tache.save()
            projet.status = sous_tache.evolution
            projet.save()


    return render(request, "pages/projet/create_sous_tache.html", { "form": form })



def create_user_view(request):

    form = UserForm()

    if request.POST:
       form = UserForm(request.POST)

       if form.is_valid:
            if request.POST.get('password') == request.POST.get('password1'):

                user = User.objects.create_user(
                    email=request.POST.get('email'),
                    contact=request.POST.get('contact'),
                    password=request.POST.get('password'),
                    first_name=request.POST.get('first_name'),
                    last_name=request.POST.get('last_name'),
                )
                form = UserForm()
                messages.add_message(request, messages.SUCCESS, "Compte créer avec succès !")
            else:
                messages.add_message(request, messages.ERROR, "Les mots de passe doivent être identiques !")
       else:
        print(False) 
    return render(request, 'pages/users/user-create.html', { 'form': form })




@login_required
def user_list_view(request):

    userlist = User.objects.all()
    return render(request, 'pages/users/user-list.html', { 'userlist': userlist })

    

def login_view(request):

    form = LoginForm()
    messages = ""
    next_url = request.GET.get('next' or None)

    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user:
                if not user.is_active:
                    user.is_active = True
                    user.save()
                login(request, user)
                messages = "Utilisateur {} est connecté !".format(request.user.last_name)

                if next_url != None:
                    redirect_path = next_url
                    if url_has_allowed_host_and_scheme(redirect_path, request.get_host()):
                        return redirect(redirect_path)

                return redirect("index")
            else:
                messages = "Mot de passe incorrect"
    return render(request, "pages/users/login.html", { 'form': form, 'message': messages })

def LogOut(request):
    
    if request.user.is_authenticated:
        logout(request)
    return redirect("index")