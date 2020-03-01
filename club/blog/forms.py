from .models import Comentario,Mensaje
from django import forms


class CommentForm(forms.Form):
    nombre = forms.CharField(max_length=50,required=True,widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'nombre'}))
    mensaje = forms.CharField(required=True,widget=forms.Textarea(attrs={'class': 'form-control','placeholder':'Mensaje'}))

    class Meta:
        model= Comentario
        fields =('nombre',',mensaje')
        
    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        if not nombre:
             raise forms.ValidationError("Nombre vacío")
        return nombre

    def clean_mensaje(self):
        mensaje = self.cleaned_data['mensaje']
        if not mensaje:
             raise forms.ValidationError("Mensaje vacío")
        return mensaje


class MensajeForm(forms.ModelForm):
    nombre = forms.CharField(max_length= 50,required=True,widget=forms.TextInput(attrs={'class':'form-control','placeholder':"Nombre"}))
    asunto = forms.CharField(max_length= 50,required=True,widget=forms.TextInput(attrs={'class':'form-control','placeholder':"Asunto"}))
    email = forms.EmailField(required=True,widget=forms.EmailInput(attrs={'class':'form-control','placeholder':"Email"}))
    body = forms.CharField(required=True,widget=forms.Textarea(attrs={'class': 'form-control','placeholder':'Mensaje'}))

    class Meta:
        model = Mensaje
        fields = ('nombre','asunto','body','email')

    def clean_nombre(self):
        if self.is_valid():
            nombre = self.cleaned_data['nombre']
            if not nombre:
                 raise forms.ValidationError("Nombre vacío")
            return nombre

    def clean_asunto(self):
        if self.is_valid():
            asunto = self.cleaned_data['asunto']
            if not asunto:
                 raise forms.ValidationError("asunto vacío")
            return asunto

    def clean_body(self):
        if self.is_valid():
            body = self.cleaned_data['body']
            if not body:
                raise  forms.ValidationError("mensaje vacío")
            return body

    def clean_email(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            if not email:
                raise  forms.ValidationError("email vacío")
            return email
