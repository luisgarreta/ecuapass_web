
import json, os, re
from os.path import join

from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import View
from django.templatetags.static import static        # For URL of static files
from django.conf import settings  # For load static settings

# Own imports
from ecuapassdocs.ecuapassutils.resourceloader import ResourceLoader 
from ecuapassdocs.ecuapassutils.pdfcreator import CreadorPDF 
from .models import CartaporteDoc, Cartaporte
#from .views_options import EmpresaOptionsView # For combo box options ini form input fields 

#
# Create your views here.
#
def index (request):
	return (render (request, "creador/index.html", {}))
	
#--------------------------------------------------------------------
#-- Clase para manejar las solicitudes de cartaporte
#--------------------------------------------------------------------
class CartaporteView (View):
	cartaporteDoc = None
	template_name = "creador/cartaporte-forma.html"

	#-------------------------------------------------------------------
	# Usado para llenar una forma (cartaporte) vacia
	# Envía los parámetros o restricciones para cada campo en la forma de HTML
	#-------------------------------------------------------------------
	def get (self, request, *args, **kargs):
		# Load parameters from package
		cartaporteParametersForFields = ResourceLoader.loadJson ("form-cartaporte", "cartaporte_parameters_for_fields.json")
		# Send input fields parameters (bounds, maxLines, maxChars, ...)
		contextDic = {"input_params" : cartaporteParametersForFields}

		return render (request, "creador/cartaporte-forma.html", contextDic)
	
	#-------------------------------------------------------------------
	# Used to receive a filled cartaporte form and create a response
	#-------------------------------------------------------------------
	@csrf_protect
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
	#-- Guarda los campos del documento cartaporte (incluye numero) a la BD
	#-------------------------------------------------------------------
	def saveDocumentToDB (self, inputValues, fieldValues, flagSave):
		# Create cartaporteDoc and save it to get id
		if flagSave == "GET-ID":
			# Save Cartaporte document
			cartaporteDoc = CartaporteDoc ()
			cartaporteDoc.save ()
			cartaporteDoc.numero = self.getCartaporteNumber (cartaporteDoc.id)
			cartaporteDoc.save ()

			# Save Cartaporte register
			cartaporteReg = Cartaporte ()
			cartaporteReg.setValues (cartaporteDoc, fieldValues)
			cartaporteReg.save ()

			return cartaporteDoc.numero
		elif flagSave == "SAVE-DATA":
			# Retrieve instance and save Cartaporte document
			docNumber = inputValues ["txt00"]
			cartaporteDoc = get_object_or_404 (CartaporteDoc, numero=docNumber)

			# Assign values to the attributes using dictionary keys
			for key, value in inputValues.items():
				setattr(cartaporteDoc, key, value)

			cartaporteDoc.save ()

			# Retrieve and save Cartaporte register
			cartaporteReg = get_object_or_404 (Cartaporte, numero=docNumber)
			cartaporteReg.setValues (cartaporteDoc, fieldValues)
			cartaporteReg.save ()

			return inputValues

	#-- Create a formated cartaporte number ranging from 2000000 
	def getCartaporteNumber (self, id):
		numero = f"CO{2000000 + id}"
		return (numero)
		
	#-------------------------------------------------------------------
	#-- Create a PDF from document
	#-------------------------------------------------------------------
	def createPDF (self, inputValues, button_type):
		creadorPDF = CreadorPDF ("cartaporte")

		print (">>> createPDF: txt00:", inputValues ["txt00"])
		outPdfPath, outJsonPath = creadorPDF.crearCartaportePDF (inputValues, button_type)

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
		gastosDic = {"value": {"ValorFlete":{"value":{}}, 
		                       "Seguro":{"value":{}}, 
							   "OtrosGastos":{"value":{}}, 
							   "Total":{"value":{}}}}

		# Load parameters from package
		cartaporteParametersForInputs = ResourceLoader.loadJson ("form-cartaporte", "cartaporte_parameters_for_inputs.json")

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

from .models import Empresa

class EmpresaOptionsView (View):
	@csrf_protect
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



