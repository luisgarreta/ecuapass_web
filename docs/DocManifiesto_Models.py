import os, tempfile, json
from datetime import date

from django.db import models

from ecuapassdocs.ecuapassinfo.ecuapass_utils import Utils
from ecuapassdocs.ecuapassinfo.ecuapass_info_manifiesto_BYZA import ManifiestoByza

class Conductor (models.Model):
	documento        = models.CharField (max_length=20)
	nombre           = models.CharField (max_length=50)
	nacionalidad     = models.CharField (max_length=50)
	licencia         = models.CharField (max_length=50)
	fecha_nacimiento = models.CharField (max_length=50)

	class Meta:
		verbose_name_plural = "Conductores"

	def __str__ (self):
		return f"{self.nombre}"

class Vehiculo (models.Model):
	placa       = models.CharField (max_length=50)
	marca       = models.CharField (max_length=100)
	pais        = models.CharField (max_length=20)
	chasis      = models.CharField (max_length=50)
	anho        = models.CharField (max_length=20)

	def __str__ (self):
		return f"{self.marca}, {self.placa}, {self.pais}"
	
class ManifiestoDoc (models.Model):
	numero = models.CharField (max_length=20)

	txt00 = models.CharField (max_length=20, default="PRELIMINAR")
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
	txt13 = models.CharField (max_length=200)
	txt14 = models.CharField (max_length=200)
	txt15 = models.CharField (max_length=200)
	txt16 = models.CharField (max_length=200)
	txt17 = models.CharField (max_length=200)
	txt18 = models.CharField (max_length=200)
	txt19 = models.CharField (max_length=200)
	txt20 = models.CharField (max_length=200)
	txt21 = models.CharField (max_length=200)
	txt22 = models.CharField (max_length=200)
	txt23 = models.CharField (max_length=200)
	txt24 = models.CharField (max_length=200)
	txt25_1 = models.CharField (max_length=200)
	txt25_2 = models.CharField (max_length=200)
	txt25_3 = models.CharField (max_length=200)
	txt25_4 = models.CharField (max_length=200)
	txt25_5 = models.CharField (max_length=200)
	txt26 = models.CharField (max_length=200)
	txt27 = models.CharField (max_length=200)
	txt28 = models.CharField (max_length=200)
	txt29 = models.CharField (max_length=200)
	txt30 = models.CharField (max_length=200)
	txt31 = models.CharField (max_length=200)
	txt32_1 = models.CharField (max_length=200)
	txt32_2 = models.CharField (max_length=200)
	txt32_3 = models.CharField (max_length=200)
	txt32_4 = models.CharField (max_length=200)
	txt33_1 = models.CharField (max_length=200)
	txt33_2 = models.CharField (max_length=200)
	txt34 = models.CharField (max_length=200)
	txt35 = models.CharField (max_length=200)
	txt36 = models.CharField (max_length=200)
	txt37 = models.CharField (max_length=200)
	txt38 = models.CharField (max_length=200)
	txt39 = models.CharField (max_length=200)
	txt40 = models.CharField (max_length=200)

	def __str__ (self):
		return f"Id: {self.id}, Numero: {self.numero} {self.txt03}"
	
	def getNumberFromId (self):
		numero = 2000000+ self.numero 
		numero = f"CO{numero}"
		return (self.numero)
		
class Manifiesto (models.Model):
	numero     = models.CharField (max_length=20)
	vehiculo   = models.ForeignKey (Vehiculo, on_delete=models.DO_NOTHING, related_name='vehiculo', null=True)
	remolque   = models.ForeignKey (Vehiculo, on_delete=models.DO_NOTHING, related_name='remolque', null=True)
	documento  = models.OneToOneField (ManifiestoDoc, on_delete=models.DO_NOTHING)
	fecha_emision = models.DateField (default=date.today)

	def __str__ (self):
		return f"{self.numero}, {self.vehiculo}"

	def setValues (self, manifiestoDoc, fieldValues):
		print (">>> manifiestoDoc:", manifiestoDoc)
		self.numero    = manifiestoDoc.numero
		self.vehiculo  = self.getVehiculo (fieldValues, "vehiculo")
		self.remolque  = self.getVehiculo (fieldValues, "remolque")
		self.documento = manifiestoDoc
		
	def getVehiculo (self, fieldValues, vehicleType):
		try:
			jsonFieldsPath, runningDir = self.createTemporalJson (fieldValues)
			manifiestoInfo             = ManifiestoByza (jsonFieldsPath, runningDir)
			info                       = manifiestoInfo.getVehiculoRemolqueInfo (vehicleType)
			print (">>> Vehículo Info:", info)

			if any (value is None for value in info.values()):
				return None
			else:
				vehiculo, created = Vehiculo.objects.get_or_create (placa=info['placa'])

				vehiculo.marca       = info ["marca"]
				vehiculo.placa       = info ["placa"]
				vehiculo.pais        = info ["pais"]
				vehiculo.chasis      = info ["chasis"]
				vehiculo.anho        = info ["anho"]
				vehiculo.certificado = info ["certificado"]

				vehiculo.save ()
				return vehiculo
		except:
			Utils.printException (f"Obteniedo información del vehiculo.")
			return None

	def createTemporalJson (self, fieldValues):
		tmpPath        = tempfile.gettempdir ()
		jsonFieldsPath = os.path.join (tmpPath, f"CARTAPORTE-{self.numero}.json")
		json.dump (fieldValues, open (jsonFieldsPath, "w"))
		return (jsonFieldsPath, tmpPath)

