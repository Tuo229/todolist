from django import forms
from .models import User, Projet, SousTache


class LoginForm(forms.Form):

    email = forms.EmailField(label="Email", required=True, widget=forms.EmailInput)
    password = forms.CharField(label="Mot de Passe", required=True, widget=forms.PasswordInput)

    def clean(self):

        data = self.cleaned_data
        email = self.cleaned_data.get('email')
        if email and "@" in email:
            user = User.objects.filter(email=email)
            if len(user) != 1:
                raise forms.ValidationError("Non utilisateur incorrecte !")
        return data


class UserForm(forms.ModelForm):

    password = forms.CharField(label="Mot de Passe", widget=forms.PasswordInput)
    password1 = forms.CharField(label="Confirmation", widget=forms.PasswordInput)

    class Meta:

        model = User

        fields = [
            "email",
            "last_name",
            "first_name",
            "contact",
            "password",
            "password1"
        ]

class ProjetForm(forms.ModelForm):
    
    date_debut = forms.DateTimeField(label="Date de dédut", required=True, widget=forms.DateTimeInput(
        attrs={
            "type": "datetime-local"
        }
    ))
    date_fin = forms.DateTimeField(label="Date de fin", required=True, widget=forms.DateTimeInput(
        attrs={
            "type": "datetime-local"
        }
    ))

    class Meta:

        model = Projet
     
        fields = (
            "libelle", "date_debut", "date_fin"
        )

class UpdateProjetForm(forms.ModelForm):

    
    class Meta:

        model = Projet
        fields = [
            "libelle", "date_fin"
        ]

class SousTacheForm(forms.ModelForm):

    date_debut = forms.DateTimeField(label="Date de debut", required=True, widget=forms.DateTimeInput(
        attrs={
            "type": "datetime-local"
        }
    ))
    date_fin = forms.DateTimeField(label="Date de fin", required=True, widget=forms.DateTimeInput(
        attrs={
            "type": "datetime-local"
        }
    ))

    class Meta:

        model = SousTache
        fields = [
            "nom_tache", "executant",
            "date_debut", "date_fin"
        ]