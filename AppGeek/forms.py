# pylint: disable=no-member
from django import forms
from .models import Categoria, Producto, Cliente, Comments, Trekking
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit


class LoginForm(forms.Form):
    username = forms.CharField(label="Usuario")
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            'username',
            'password',
            Submit('submit', 'Acceder', css_class='btn-primary')
        )


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'categoria', 'stock', 'precio', 'imagen']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria'].queryset = Categoria.objects.all()
        self.fields['categoria'].label_from_instance = lambda obj: obj.nombre
        self.fields['categoria'].empty_label = None
        for field_name, field in self.fields.items():
            field.widget.attrs['readonly'] = True


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'email', 'direccion', 'fecha_nacimiento']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['content', 'imagen', 'estado']
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Escribe tu comentario'}),
        }

    def __init__(self, trekking, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['imagen'].required = False
        self.fields['estado'].initial = trekking.estado

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get('content')
        estado = cleaned_data.get('estado')

        # Obtener el estado inicial desde trekking
        estado_inicial = self.fields['estado'].initial

        # Verificar si no hay contenido y se cambió el estado
        if not content and estado and estado != estado_inicial:
            # Cambiar el valor de 'content' solo si hay un cambio de estado
            cleaned_data['content'] = f'Cambio de estado: {estado_inicial} -> {estado}'

        return cleaned_data


class BusquedaForm(forms.Form):
    query = forms.CharField(label='Buscar Producto', max_length=100)


class TrekkingForm(forms.ModelForm):
    class Meta:
        model = Trekking
        exclude = ['usuario', 'fecha_cierre', 'duracion_dias', 'dificultad']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
        }