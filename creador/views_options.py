
from django.http import JsonResponse
from django.views import View

# For textarea options
from django.db.models import Q
#from dal import autocomplete

from .models import Empresa

#-- Class for autocomplete options while the user is typing
class EmpresaOptionsView (View):
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



