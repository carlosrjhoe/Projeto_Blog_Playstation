from django.forms import ModelForm
from .models import Comentario


class FormComentario(ModelForm):

    def clean(self):
        """Validação de comentario do post"""
        data = self.cleaned_data
        nome = data.get('nome_comentario')
        email = data.get('email_comentario')
        comentario = data.get('comentario')

        if len(nome) < 5:
            """Validação do tamanho do nome do comentario do post"""
            self.add_error(
                'nome_comentario',
                'Nome precisa ter mais de 5 caracteres.'
            )

        if not comentario:
            """Validação de comentário"""
            self.add_error(
                'comentario',
                'Você não comentou.'
            )
            
        if not email:
            """Validação do email"""
            self.add_error(
                'email_comentario',
                'E-mail não cadastrado, Obrigatório o cadastro do e-mail!'
            )

    class Meta:
        model = Comentario
        fields = ('nome_comentario', 'email_comentario', 'comentario')
