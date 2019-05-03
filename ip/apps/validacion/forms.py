from django import forms

from apps.validacion.models import Campos_defecto


class Campos_defectoForm(forms.ModelForm):
    class Meta:
        model = Campos_defecto


        fields = [
            'imagen',
            'tag',
            'precision',
            'v_esperado',
            'medidas',
            'user'
        ]

        labels = {
            'imagen': "Tipo de imágen",
            'tag': "Nombre del tag (Dicom)",
            'precision':"Toleracia (%)",
            'v_esperado': "Valor Esperado",
            'medidas': "Unidades de medida",

        }
        widgets = {
            'imagen': forms.Select(attrs={'class': 'form-control'}),
            'tag': forms.Select(attrs={'class': 'form-control'}),
            'precision': forms.TextInput(attrs={'class': 'form-control', 'maxlength':3,'autocomplete':"off", 'placeholder': ('Entre 0 y 100'),'oninput': "this.value = this.value.replace(/[^0-9]/, '')"}),
            'v_esperado': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': "off"}),
            'medidas':forms.TextInput(attrs={'class': 'form-control', 'autocomplete': "off"}),
            'user': forms.HiddenInput(),
        }
        
        
class SeleccionForm(forms.Form):
    lista_img = forms.CharField(max_length = 500)
    picture_pk = forms.CharField(max_length = 100)