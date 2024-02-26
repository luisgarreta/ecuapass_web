
import json, os, re, datetime
from os.path import join

from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.urls import resolve   # To get calling URLs
from django.shortcuts import get_object_or_404, render
from django.views import View

# For CSRF protection
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

# For textarea options
from django.db.models import Q

# Own imports
from ecuapassdocs.ecuapassinfo.resourceloader import ResourceLoader 
from .views_EcuapassDocView import EcuapassDocView
from .models import Cartaporte, CartaporteDoc, Manifiesto, Vehiculo, Conductor

#--------------------------------------------------------------------
#-- Vista para manejar las solicitudes de manifiesto
#--------------------------------------------------------------------
class ManifiestoDocView (EcuapassDocView):
	document_type    = "manifiesto"
	template_name    = "doc_forma_manifiesto.html"
	background_image = "appdocs/images/image-manifiesto-vacio-NTA-BYZA.png"
	parameters_file  = "manifiesto_input_parameters.json"

	def __init__(self, *args, **kwargs):
		# Load parameters from package
		self.inputParameters = ResourceLoader.loadJson ("docs", self.parameters_file)
		super().__init__ (self.document_type, self.template_name, self.background_image, 
		                  self.parameters_file, self.inputParameters, *args, **kwargs)

	#-- Set constant values for the BYZA company
	def setInitialValuesToInputs (self, request):
		super ().setInitialValuesToInputs (request)

		# Permisos values for BYZA 
		self.inputParameters ["txt02"]["value"] = "PO-CO-0033-22"
		self.inputParameters ["txt03"]["value"] = "PO-CO-0033-22"

#--------------------------------------------------------------------
#-- Class for autocomplete options while the user is typing
#--------------------------------------------------------------------
#--------------------------------------------------------------------
# Show all 'cartaportes' from current date (selected in manifiesto)
# Return all "mercancia" info (nro cartaporte, descripcion, ..., totals
# It doesn't totalize peso "bruto", "neto", and "otras"
#--------------------------------------------------------------------
class CartaporteOptionsView (View):
	@method_decorator(csrf_protect)
	def get (self, request, *args, **kwargs):
		print ("--get CartaporteOptionsView")
		itemOptions = []
		try:
			# Get cartaporte docs from query
			query = request.GET.get ('query', '')
			current_date = datetime.date.today()    
			currentCartaportes = Cartaporte.objects.filter (numero__startswith=query,
															fecha_emision=current_date)
			docsCartaportes = [model.documento.__dict__ for model in currentCartaportes]

			for i, doc in enumerate (docsCartaportes):
				itemLine = f"{i}. {doc['numero']}"
				itemText = "%s||%s||%s||%s||%s||%s||%s||%s||%s||%s||%s" % ( 
							doc ['numero'],  # Cartaporte
							doc ["txt12"],   # Descripcion 
							doc ["txt10"],   # Cantidad
							doc ["txt11"],   # Marca
							doc ["txt13_2"], # Peso bruto
							doc ["txt13_1"], # Peso neto
							doc ["txt15"],   # Otras unidades
							re.sub (r'[\r\n]+\s*', '. ', doc ["txt16"]), # INCONTERMS
							doc ["txt13_2"], # Peso bruto total
							doc ["txt13_1"], # Peso neto total
							doc ["txt15"])   # Otras unidades total

				newOption = {"itemLine" : itemLine, "itemText" : itemText}
				print ("--itemLine:", itemLine)
				print ("--itemText:", itemText)
				itemOptions.append (newOption)
		except:
			print (">>> Excepcion obteniendo opciones de cartaportes")
			
		return JsonResponse (itemOptions, safe=False)

##--------------------------------------------------------------------
## Show options when user types in "input_placaPais"
##--------------------------------------------------------------------
#class VehiculoOptionsView (View):
#	@method_decorator(csrf_protect)
#	def get (self, request, *args, **kwargs):
#		query = request.GET.get('query', '')
#		options = Vehiculo.objects.filter (placa__istartswith=query).values()
#
#		itemOptions = []
#		for i, option in enumerate (options):
#			itemLine = f"{i}. {option['placa']}"
#			itemText = "%s||%s||%s. %s||%s" % (option["marca"], option["anho"], 
#			            option["placa"], option ["pais"], option ["chasis"])
#			newOption = {"itemLine" : itemLine, "itemText" : itemText}
#			itemOptions.append (newOption)
#		
#		return JsonResponse (itemOptions, safe=False)
#
##--------------------------------------------------------------------
## Show options when user types in "input_placaPais"
##--------------------------------------------------------------------
#class ConductorOptionsView (View):
#	@method_decorator(csrf_protect)
#	def get (self, request, *args, **kwargs):
#		query = request.GET.get('query', '')
#		options = Conductor.objects.filter (nombre__istartswith=query).values()
#
#		itemOptions = []
#		for i, option in enumerate (options):
#			itemLine = f"{i}. {option['nombre']}"
#			itemText = "%s||%s||%s||%s||%s" % (option["nombre"], option["documento"], 
#			           option["nacionalidad"], option ["licencia"], option ["fecha_nacimiento"])
#			newOption = {"itemLine" : itemLine, "itemText" : itemText}
#			itemOptions.append (newOption)
#		
#		return JsonResponse (itemOptions, safe=False)
#
#
