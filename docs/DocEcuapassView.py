
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
from ecuapassdocs.ecuapassutils.pdfcreator import CreadorPDF 
#from .pdfcreator import CreadorPDF

#--------------------------------------------------------------------
#-- Vista para manejar las solicitudes de manifiesto
#--------------------------------------------------------------------
class DocEcuapassView (View):

	def __init__(self, docType, templateName, parametersFile, *args, **kwargs):
		super().__init__ (*args, **kwargs)
		self.docType        = docType
		self.templateName   = templateName
		self.parametersFile = parametersFile

	#-------------------------------------------------------------------
	# Usado para llenar una forma (manifiesto) vacia
	# Envía los parámetros o restricciones para cada campo en la forma de HTML
	#-------------------------------------------------------------------
	def get (self, request, *args, **kargs):
		# Load parameters from package
		inputParameters = ResourceLoader.loadJson ("docs", self.parametersFile)
		# Send input fields parameters (bounds, maxLines, maxChars, ...)
		contextDic = {"input_parameters" : inputParameters}

		return render (request, self.templateName, contextDic)
	
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
		else:
			print (">>> Error: No se conoce opción del botón presionado:", button_type)
				
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
		inputParameters = ResourceLoader.loadJson ("docs", self.parametersFile)

		for key, params in inputParameters.items():
			fieldName    = params ["field"]
			value        = inputValues [key]
			jsonFieldsDic [fieldName] = {"value": value, "content": value}

		return jsonFieldsDic

	#-------------------------------------------------------------------
	#-- Create a PDF from document
	#-------------------------------------------------------------------
	def createPDF (self, inputValues, button_type):
		creadorPDF = CreadorPDF (self.docType)

		print (">>> createPDF: txt00:", inputValues ["txt00"])
		#print (inputValues)
		outPdfPath, outJsonPath = creadorPDF.createPdfDocument (inputValues, button_type)
		#print (">>> Outputs:", outPdfPath, outJsonPath)

		# Respond with the output PDF
		with open(outPdfPath, 'rb') as pdf_file:
			pdfContent = pdf_file.read()

		return (os.path.basename (outPdfPath), pdfContent)

