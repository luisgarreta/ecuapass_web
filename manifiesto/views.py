
import json, os, re
from os.path import join

from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views import View


from django.templatetags.static import static        # For URL of static files
from django.conf import settings  # For load static settings

# For CSRF protection
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

# Own imports
from ecuapassdocs.ecuapassutils.resourceloader import ResourceLoader 
from ecuapassdocs.ecuapassutils.pdfcreator import CreadorPDF 
from .models import ManifiestoDoc, Manifiesto

def index (request):
	return (render (request, "creador/index.html", {}))
#--------------------------------------------------------------------
#-- Vista para manejar las solicitudes de manifiesto
#--------------------------------------------------------------------
class ManifiestoView (View):
	manifiestoDoc = None
	template_name = "manifiesto-forma.html"

	#-------------------------------------------------------------------
	# Usado para llenar una forma (manifiesto) vacia
	# Envía los parámetros o restricciones para cada campo en la forma de HTML
	#-------------------------------------------------------------------
	def get (self, request, *args, **kargs):
		# Load parameters from package
		manifiestoParametersForFields = ResourceLoader.loadJson ("docs", "manifiesto_input_parameters.json")
		# Send input fields parameters (bounds, maxLines, maxChars, ...)
		contextDic = {"input_parameters" : manifiestoParametersForFields}

		return render (request, "manifiesto-forma.html", contextDic)
	
	#-------------------------------------------------------------------
	# Used to receive a filled manifiesto form and create a response
	#-------------------------------------------------------------------
	@method_decorator(csrf_protect)
	def post (self, request, *args, **kargs):
		# Get values from html form
		button_type = request.POST.get('boton_pdf', '').lower()

		inputValues = self.getInputValuesFromForm (request)       # Values without CPI number
		fieldValues = self.getFieldValuesFromBounds (inputValues)
		docNumber   = inputValues ["txt00"]

		pdfFilename, pdfContent  = self.createPDF  (inputValues, button_type)

		# Prepare and return HTTP response for PDF
		pdf_response = HttpResponse (content_type='application/pdf')
		pdf_response ['Content-Disposition'] = f'inline; filename="{pdfFilename}"'
		pdf_response.write (pdfContent)

		if "preliminar" in button_type:
			return pdf_response
		elif "original" in button_type:
			if docNumber == "" or docNumber == "CLON" or docNumber == "PRELIMINAR": 
				docNumber     = self.saveDocumentToDB (inputValues, fieldValues, "GET-ID")
				return JsonResponse ({'numero': docNumber}, safe=False)
			else: 
				self.saveDocumentToDB (inputValues, fieldValues, "SAVE-DATA")
				return pdf_response
		elif "copia" in button_type:
			if inputValues ["txt00"] != "": 	
				return pdf_response
			else: 
				response_data      = {'message': "Error: No se ha creado documento original!" }
				return JsonResponse(response_data, safe=False)
		elif "clonar" in button_type:
			response_data      = {'numero': "CLON"}
			return JsonResponse(response_data, safe=False)
				
	#-------------------------------------------------------------------
	#-- Guarda los campos del documento manifiesto (incluye numero) a la BD
	#-------------------------------------------------------------------
	def saveDocumentToDB (self, inputValues, fieldValues, flagSave):
		# Create manifiestoDoc and save it to get id
		if flagSave == "GET-ID":
			# Save Manifiesto document
			manifiestoDoc = ManifiestoDoc ()
			manifiestoDoc.save ()
			manifiestoDoc.numero = self.getManifiestoNumber (manifiestoDoc.id)
			manifiestoDoc.save ()

			# Save Manifiesto register
			manifiestoReg = Manifiesto ()
			manifiestoReg.setValues (manifiestoDoc, fieldValues)
			manifiestoReg.save ()

			return manifiestoDoc.numero
		elif flagSave == "SAVE-DATA":
			# Retrieve instance and save Manifiesto document
			docNumber = inputValues ["txt00"]
			manifiestoDoc = get_object_or_404 (ManifiestoDoc, numero=docNumber)

			# Assign values to the attributes using dictionary keys
			for key, value in inputValues.items():
				setattr(manifiestoDoc, key, value)

			manifiestoDoc.save ()

			# Retrieve and save Manifiesto register
			manifiestoReg = get_object_or_404 (Manifiesto, numero=docNumber)
			manifiestoReg.setValues (manifiestoDoc, fieldValues)
			manifiestoReg.save ()

			return inputValues

	#-- Create a formated manifiesto number ranging from 2000000 
	def getManifiestoNumber (self, id):
		numero = f"CO{2000000 + id}"
		return (numero)
		
	#-------------------------------------------------------------------
	#-- Create a PDF from document
	#-------------------------------------------------------------------
	def createPDF (self, inputValues, button_type):
		creadorPDF = CreadorPDF ("manifiesto")

		print (">>> createPDF: txt00:", inputValues ["txt00"])
		outPdfPath, outJsonPath = creadorPDF.createPdfDocument (inputValues, button_type)

		# Respond with the output PDF
		with open(outPdfPath, 'rb') as pdf_file:
			pdfContent = pdf_file.read()

		return (os.path.basename (outPdfPath), pdfContent)

	#-------------------------------------------------------------------
	#-- Return a dic with the texts from the document form (e.g. txt00,)
	#-------------------------------------------------------------------
	def getInputValuesFromForm (self, request):
		inputValues = {}
		for key in request.POST:
			if key.startswith ("txt"):
				inputValues [key] = request.POST [key]

		inputValues ["numero"] = inputValues ["txt00"]

		return inputValues

	#----------------------------------------------------------------
	#-- Embed fields info (key:value) into PDF doc
	#-- Info is embedded according to Azure format
	#----------------------------------------------------------------
	def getFieldValuesFromBounds (self, inputValues):
		jsonFieldsDic = {}
		# Load parameters from package
		manifiestoParametersForInputs = ResourceLoader.loadJson ("docs", "manifiesto_input_parameters.json")

		for key, params in manifiestoParametersForInputs.items():
			fieldName    = params ["field"]
			value        = inputValues [key]
			jsonFieldsDic [fieldName] = {"value": value, "content": value}

		return jsonFieldsDic

#--------------------------------------------------------------------
#-- Class for autocomplete options while the user is typing
#--------------------------------------------------------------------
# For textarea options
from django.db.models import Q
#from dal import autocomplete

from .models import Vehiculo

class VehiculoOptionsView (View):
	@method_decorator(csrf_protect)
	def get (self, request, *args, **kwargs):
		print (">>> In get from VehiculoOptionsView")
		query = request.GET.get('query', '')
		options = Vehiculo.objects.filter (placa__icontains=query).values()

		itemOptions = []
		for i, option in enumerate (options):
			itemLine = f"{i}. {option['placa']}"
			itemText = "%s||%s||%s. %s||%s" % (option["marca"], option["anho"], option["placa"], option ["pais"], option ["chasis"])
			newOption = {"itemLine" : itemLine, "itemText" : itemText}
			itemOptions.append (newOption)
		

		return JsonResponse (itemOptions, safe=False)



