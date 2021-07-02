from django import forms
from .models import Chem

class ChemForm(forms.ModelForm):
	class Meta:
		model = Chem
		fields = '__all__'
