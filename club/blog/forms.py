from .models import Comentario,Mensaje
from django import forms


class CommentForm(forms.Form):
    nombre = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'nombre'}))
    mensaje = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control','placeholder':'Mensaje'}))

class MensajeForm(forms.ModelForm):
    nombre = forms.CharField(max_length= 50,required=True,widget=forms.TextInput(attrs={'class':'form-control','placeholder':"Nombre"}))
    asunto = forms.CharField(max_length= 50,required=True,widget=forms.TextInput(attrs={'class':'form-control','placeholder':"Asunto"}))
    email = forms.EmailField(required=True,widget=forms.EmailInput(attrs={'class':'form-control','placeholder':"Email"}))
    body = forms.CharField(required=True,widget=forms.Textarea(attrs={'class': 'form-control','placeholder':'Mensaje'}))

    class Meta:
        model = Mensaje
        fields = ['nombre','asunto','email','body']
