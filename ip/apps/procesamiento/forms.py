from django import forms

from apps.procesamiento.models import Taskgroup, Task, Pipeline


    
class gruposForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super().__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['dependencia'].required = False
    
    class Meta:
        model = Taskgroup


        fields = [
            'nombre',
            'tipo_imagen',
            'orden',
            'dependencia',

        ]

        labels = {
            'nombre':"Nombre",
            'orden':"Orden",
            'tipo_imagen':"Tipo de Imagen",
            'dependencia':"Dependencia",


        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': "off"}),
            'orden': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': "off"}),
            'tipo_imagen': forms.Select(attrs={'class': 'form-control'}),
            'dependencia': forms.Select(attrs={'required': 'false'}),
        }
        
class PipelineForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super().__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['dependencia'].required = False
    
    class Meta:
        model = Pipeline


        fields = [
            'nombre',
            'tipo_imagen',
            'orden',
            'dependencia',

        ]

        labels = {
            'nombre':"Nombre",
            'orden':"Orden",
            'tipo_imagen':"Tipo de Imagen",
            'dependencia':"Dependencia",


        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': "off"}),
            'orden': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': "off"}),
            'tipo_imagen': forms.Select(attrs={'class': 'form-control'}),
            'dependencia': forms.Select(attrs={'required': 'false'}),
        }
        
class MultiForm(forms.Form):
    user = forms.CharField(max_length = 100)
    lista_img = forms.CharField(max_length = 500)
    pipeline_pk = forms.CharField(max_length = 100)