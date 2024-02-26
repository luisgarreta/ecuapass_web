from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

class UsuarioEcuapassManager (BaseUserManager):
	def create_user (self, username, email, password=None, **extra_fields):
		if not email:
			raise ValueError ('El correo es obligatorio')

		email = self.normalize_email (email)
		user  = self.model (username=username.strip (), email=email, **extra_fields)
		user.set_password (password)
		user.save (using=self._db)
		return user

	def create_superuser (self, username, email, password=None, **extra_fields):
		extra_fields.setdefault ('is_staff', True)
		extra_fields.setdefault ('is_superuser', True)
		extra_fields.setdefault ('is_superuser', True)
		extra_fields.setdefault ('perfil', 'director')

		if extra_fields.get ('is_staff') is not True:
			raise ValueError ('Superuser must have is_staff=True.')
		if extra_fields.get ('is_superuser') is not True:
			raise ValueError ('Superuser must have is_superuser=True.')

		return self.create_user (username, email, password, **extra_fields)

class UsuarioEcuapass (AbstractUser):
	first_name	       = models.CharField (_ ('nombres'), max_length=50)
	last_name	       = models.CharField (_ ('apellidos'), max_length=50)
	is_active	       = models.BooleanField (_ ('activo'), default=True)
	is_staff	       = models.BooleanField (_ ('staff'), default=False)
	es_director	       = models.BooleanField (default=False)
	es_funcionario	   = models.BooleanField (default=False)
	es_externo	       = models.BooleanField (default=True)
	date_joined        = models.DateTimeField (_ ('fecha de registro'), auto_now_add=True)
	nro_docs_creados   = models.IntegerField (default=0)
	nro_docs_asignados = models.IntegerField (default=0)

	USER_TYPE_CHOICES =  (
		 ('externo', 'Externo'),
		 ('funcionario', 'Funcionario'),
		 ('director', 'Director'),
	)
	perfil = models.CharField (max_length=20, choices=USER_TYPE_CHOICES)

	username = models.CharField (_ ('nombre de usuario'), max_length=30, unique=True,
		help_text='Requerido. Letras y digitos, sin espacios ni carácteres, tildes o eñes.',
		validators=[], error_messages={ 'unique': "Este nombre de usuario ya está registrado..",},
	)
	email = models.EmailField (_ ('correo electrónico'), unique=True,
		help_text='Requerido.', 
		validators=[], error_messages={ 'unique': "Este correo ya está registrado..",},
	)

	#-------------------------------------------------------------------
	# Methods for special column "Acciones" in user model
	#-------------------------------------------------------------------
	def get_link_actualizar(self):
		return reverse('actualizar', args=[self.pk])
	def get_link_actualizar_display(self):
		return 'Actualizar'

	def get_link_eliminar(self):
		return reverse('eliminar', args=[self.pk])
	def get_link_eliminar_display(self):
		return 'Eliminar'

	#-------------------------------------------------------------------

	objects = UsuarioEcuapassManager ()
