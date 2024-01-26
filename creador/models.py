import os, tempfile, json
from datetime import date

from django.db import models

from ecuapassdocs.ecuapassinfo.ecuapass_utils import Utils
from ecuapassdocs.ecuapassinfo.ecuapass_info_cartaporte_BYZA import CartaporteByza

class TestDB2 (models.Model):
	nombre         = models.CharField (max_length=50)
	direccion     = models.CharField (max_length=100)

class TestDB (models.Model):
	nombre         = models.CharField (max_length=50)
	direccion     = models.CharField (max_length=100)

class Empresa (models.Model):
	nombre         = models.CharField (max_length=50)
	direccion     = models.CharField (max_length=100)
	ciudad         = models.CharField (max_length=50)
	pais           = models.CharField (max_length=20)
	tipoId         = models.CharField (max_length=20)
	numeroId       = models.CharField (max_length=50)

	def __str__ (self):
		return f"{self.id}, {self.nombre} {self.numeroId}"
	
class CartaporteDoc (models.Model):
	numero = models.CharField (max_length=20)
	txt00 = models.CharField (max_length=20)
	txt01 = models.CharField (max_length=200)
	txt02 = models.CharField (max_length=200)
	txt03 = models.CharField (max_length=200)
	txt04 = models.CharField (max_length=200)
	txt05 = models.CharField (max_length=200)
	txt06 = models.CharField (max_length=200)
	txt07 = models.CharField (max_length=200)
	txt08 = models.CharField (max_length=200)
	txt09 = models.CharField (max_length=200)
	txt10 = models.CharField (max_length=200)
	txt11 = models.CharField (max_length=200)
	txt12 = models.CharField (max_length=200)
	txt13_1 = models.CharField (max_length=200)
	txt13_2 = models.CharField (max_length=200)
	txt14 = models.CharField (max_length=200)
	txt15 = models.CharField (max_length=200)
	txt16 = models.CharField (max_length=200)
	txt17_11 = models.CharField (max_length=200)
	txt17_12 = models.CharField (max_length=200)
	txt17_13 = models.CharField (max_length=200)
	txt17_14 = models.CharField (max_length=200)
	txt17_21 = models.CharField (max_length=200)
	txt17_22 = models.CharField (max_length=200)
	txt17_23 = models.CharField (max_length=200)
	txt17_24 = models.CharField (max_length=200)
	txt17_31 = models.CharField (max_length=200)
	txt17_32 = models.CharField (max_length=200)
	txt17_33 = models.CharField (max_length=200)
	txt17_34 = models.CharField (max_length=200)
	txt17_41 = models.CharField (max_length=200)
	txt17_42 = models.CharField (max_length=200)
	txt17_43 = models.CharField (max_length=200)
	txt17_44 = models.CharField (max_length=200)
	txt18 = models.CharField (max_length=200)
	txt19 = models.CharField (max_length=200)
	txt20 = models.CharField (max_length=200)
	txt21 = models.CharField (max_length=200)
	txt22 = models.CharField (max_length=200)
	txt23 = models.CharField (max_length=200)
	txt24 = models.CharField (max_length=200)

	def __str__ (self):
		return f"Id: {self.id}, Numero: {self.numero} {self.txt03}"
	
	def getNumberFromId (self):
		numero = 2000000+ self.numero 
		numero = f"CO{numero}"
		return (self.numero)
		
# Create your models here.
class Cartaporte (models.Model):
	numero        = models.CharField (max_length=20)
	remitente     = models.ForeignKey (Empresa, on_delete=models.CASCADE, null=True)
	documento     = models.OneToOneField (CartaporteDoc, on_delete=models.CASCADE)
	fecha_emision = models.DateField (default=date.today)

	def setValues (self, cartaporteDoc, fieldValues):
		print (">>> cartaporteDoc:", cartaporteDoc)
		self.numero     = cartaporteDoc.numero
		self.documento  = cartaporteDoc
		self.remitente  = self.getRemitente (fieldValues)
		
	def getRemitente (self, fieldValues):
		try:
			jsonFieldsPath, runningDir = self.createTemporalJson (fieldValues)
			cartaporteInfo    = CartaporteByza (jsonFieldsPath, runningDir)
			info              = cartaporteInfo.getSubjectInfo ("02_Remitente")
			print (">>> Info:", info)

			if any (value is None for value in info.values()):
				return None
			else:
				empresa, created = Empresa.objects.get_or_create (numeroId=info['numeroId'])

				empresa.nombre    = info ["nombre"]
				empresa.direccion = info ["direccion"]
				empresa.ciudad    = info ["ciudad"]
				empresa.pais      = info ["pais"]
				empresa.tipoId    = info ["tipoId"]
				empresa.numeroId  = info ["numeroId"]

				empresa.save ()
				return empresa
		except:
			Utils.printException (f"Obteniedo info del remitente en el texto")
			return None

	def createTemporalJson (self, fieldValues):
		tmpPath        = tempfile.gettempdir ()
		jsonFieldsPath = os.path.join (tmpPath, f"CARTAPORTE-{self.numero}.json")
		json.dump (fieldValues, open (jsonFieldsPath, "w"))
		return (jsonFieldsPath, tmpPath)

	def __str__ (self):
		return f"{self.id}, {self.numero} {self.remitente}"
