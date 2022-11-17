from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from .models import Post
from django.db.models import Q, Count, Case, When

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
      numero_comentarios = Count(
        Case(
          When(comentario__publicado_comentario=True, then=1)
        )
      )
    )
    return qs

class PostBusca(PostIndex):
  pass


class PostCategoria(PostIndex):
  template_name = 'posts\post_categoria.html'


class PostDetalhes(UpdateView):
  pass
