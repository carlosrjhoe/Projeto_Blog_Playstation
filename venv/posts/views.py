from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from .models import Post
from django.db.models import Q, Count, Case, When
from comentarios.forms import FormComentario

# Create your views here.


class PostIndex(ListView):
    model = Post
    template_name = 'posts\index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        """Ordenar os post de forma invertida. Sempre o ultimo post será mostrado em 1º"""
        """(Q, Count, Case, When) Serve para contar a quantidade de comentarios"""
        qs = super().get_queryset()
        qs = qs.order_by('-id').filter(publicado_post=True)
        qs = qs.annotate(
            numero_comentarios=Count(
                Case(
                    When(comentario__publicado_comentario=True, then=1)
                )
            )
        )
        return qs


class PostBusca(PostIndex):
    """Funcionalidade de buscar palavras que contenham no post"""
    template_name = 'posts\post_busca.html'

    def get_queryset(self):
        qs = super().get_queryset()
        termo = self.request.GET.get('termo')

        if not termo:
            return qs

        qs = qs.filter(
            Q(titulo_post__icontains=termo) |
            Q(autor_post__first_name__iexact=termo) |
            Q(conteudo_post__icontains=termo) |
            Q(excerto_post__icontains=termo) |
            Q(categoria_post__nome_cat__iexact=termo)
        )

        return qs


class PostCategoria(PostIndex):
    template_name = 'posts\post_categoria.html'

    def get_queryset(self):
        """Filtrando por categoria"""
        qs = super().get_queryset()
        categoria = self.kwargs.get('categoria', None)
        if not categoria:
            return qs

        qs = qs.filter(categoria_post__nome_cat__iexact=categoria)
        return qs


class PostDetalhes(UpdateView):
    """Detalhes dos posts"""
    template_name = 'posts\post_detalhes.html'
    model = Post
    form_class = FormComentario
    context_object_name = 'post'
