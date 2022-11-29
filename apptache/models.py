from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin

# Create your models here.

class UserManager(BaseUserManager):

    use_in_migrations = True


    def _create_user(self, email, contact, password, **extra_fields):

        values = [email, contact]
        print(extra_fields)
        field_value_map = dict(zip(self.model.REQUIRED_FIELDS, values))
        for field_name, value in field_value_map.items():
            if not value:
                raise ValueError("Le champ {} doit etre rempli".format(field_name))
        
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            contact=contact,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, contact, password=None, **extra_fields):
        
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_active') is not True:
            raise ValueError("Une lié au droit d'accès c'est produite")

        return self._create_user(email, contact, password, **extra_fields)


    def create_superuser(self, email, contact, password=None, **extra_fields):

        extra_fields.setdefault('is_staff', True),
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Le champ is staff ne pas être faux pour l'admin")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Le champ is superuser ne pas être faux pour l'admin")
        if extra_fields.get('is_active') is not True:
            raise ValueError("Le champ is active ne pas être faux pour l'admin")

        return self._create_user(email, contact, password, **extra_fields)


    
class User(AbstractBaseUser, PermissionsMixin):
    last_name = models.CharField("Prénom", max_length=255)
    email = models.EmailField(max_length=60, unique=True)
    first_name = models.CharField("Nom", max_length=30)
    contact = models.CharField(max_length=15, unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser  = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    username = None

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['contact']
    
    def __str__(self):
        return self.email


class Projet(models.Model):

    libelle = models.CharField(max_length=255)
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    status = models.CharField(max_length=56, default="En attente")
    owner = models.ForeignKey(User, verbose_name="Proprietaire", on_delete=models.CASCADE)



STATUS_TACHE = (
    ('ATTENTE', "En attente"),
    ('COURS', "En cours"),
    ("TERMINER", "Terminer"),
    ("ABANDON", "Abandon"),
    ("ANNULER", "Annuler"),
)

class SousTacheManager(models.Manager):

    def deviner_etiquette(self, projet):

        obj_sous_tache = self.get_queryset().filter(projet=projet)
        if len(obj_sous_tache) != 0:
            lettre_num = ord('A') + len(obj_sous_tache)
            lettre = chr(lettre_num)
            return lettre
        return "A"


class SousTache(models.Model):

    etiquette = models.CharField(max_length=5)
    couleur = models.CharField(max_length=56)
    nom_tache = models.CharField(max_length=256)
    executant = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    evolution = models.CharField(max_length=56, choices=STATUS_TACHE, default="En attente")
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE)
    objects = SousTacheManager()
