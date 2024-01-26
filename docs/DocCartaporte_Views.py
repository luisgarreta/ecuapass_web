
import json, os, re
from os.path import join

from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views import View

# For CSRF protection
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

# Own imports
from ecuapassdocs.ecuapassutils.resourceloader import ResourceLoader 

from .DocEcuapassView import DocEcuapassView
from .DocCartaporte_Models import CartaporteDoc, Cartaporte, Empresa

def index (request):
	return (render (request, "creador/index.html", {}))
#--------------------------------------------------------------------
#-- Vista para manejar las solicitudes de manifiesto
#--------------------------------------------------------------------
class DocCartaporteView (DocEcuapassView):
	template_name = "cartaporte-forma.html"

	def __init__(self, *args, **kwargs):
		super().__init__ ("cartaporte", "cartaporte-forma.html", "cartaporte_input_parameters.json", *args, **kwargs)

	#-------------------------------------------------------------------
	#-- Guarda los campos del documento manifiesto (incluye numero) a la BD
	#-------------------------------------------------------------------
	def saveDocumentToDB (self, inputValues, fieldValues, flagSave):
		# Create ecuapassDoc and save it to get id
		if flagSave == "GET-ID":
			# Save Cartaporte document
			ecuapassDoc = CartaporteDoc ()
			ecuapassDoc.save ()
			ecuapassDoc.numero = self.getManifiestoNumber (ecuapassDoc.id)
			ecuapassDoc.save ()

			# Save Cartaporte register
			manifiestoReg = Cartaporte ()
			manifiestoReg.setValues (ecuapassDoc, fieldValues)
			manifiestoReg.save ()

			return ecuapassDoc.numero
		elif flagSave == "SAVE-DATA":
			# Retrieve instance and save Cartaporte document
			docNumber = inputValues ["txt00"]
			ecuapassDoc = get_object_or_404 (CartaporteDoc, numero=docNumber)

			# Assign values to the attributes using dictionary keys
			for key, value in inputValues.items():
				setattr(ecuapassDoc, key, value)

			ecuapassDoc.save ()

			# Retrieve and save Cartaporte register
			manifiestoReg = get_object_or_404 (Cartaporte, numero=docNumber)
			manifiestoReg.setValues (ecuapassDoc, fieldValues)
			manifiestoReg.save ()

			return inputValues

	#-- Create a formated manifiesto number ranging from 2000000 
	def getManifiestoNumber (self, id):
		numero = f"CO{2000000 + id}"
		return (numero)
		
	#----------------------------------------------------------------
	#-- Embed fields info (key:value) into PDF doc
	#-- Info is embedded according to Azure format
	#----------------------------------------------------------------
	def getFieldValuesFromBounds (self, inputValues):
		jsonFieldsDic = {}
		gastosDic = {"value": {"ValorFlete":{"value":{}}, 
		                       "Seguro":{"value":{}}, 
							   "OtrosGastos":{"value":{}}, 
							   "Total":{"value":{}}}}

		# Load parameters from package
		cartaporteParametersForInputs = ResourceLoader.loadJson ("docs", self.parametersFile)

		for key, params in cartaporteParametersForInputs.items():
			fieldName    = params ["field"]
			value        = inputValues [key]
			if "Gastos" in fieldName:
				res = re.findall ("\w+", fieldName)   #e.g ["ValorFlete", "MontoDestinatario"]
				tableName, rowName, colName = res [0], res [1], res[2]
				if value != "":
					gastosDic ["value"][rowName]["value"][colName] = {"value": value, "content": value}
			else:
				jsonFieldsDic [fieldName] = {"value": value, "content": value}

		jsonFieldsDic [tableName] = gastosDic
		return jsonFieldsDic

#--------------------------------------------------------------------
#-- Class for autocomplete options while the user is typing
#--------------------------------------------------------------------
# For textarea options
from django.db.models import Q
#from dal import autocomplete

#from .models import Empresa

class EmpresaOptionsView (View):
	@method_decorator(csrf_protect)
	def get (self, request, *args, **kwargs):
		query = request.GET.get('query', '')
		options = Empresa.objects.filter (nombre__icontains=query).values()

		itemOptions = []
		for i, option in enumerate (options):
			itemLine = f"{i}. {option['nombre']}"
			itemText = "%s\n%s\n%s-%s. %s:%s" % (
			              option["nombre"], option ["direccion"], 
						  option ["ciudad"], option ["pais"],
						  option ["tipoId"], option ["numeroId"])

			newOption = {"itemLine" : itemLine, "itemText" : itemText}
			itemOptions.append (newOption)
		

		return JsonResponse (itemOptions, safe=False)



