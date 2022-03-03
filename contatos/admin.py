from django.contrib import admin

from .models import Categoria, Contato

class ContatoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'sobrenome', 'mostrar', 'telefone')
    list_display_links = ('sobrenome',)
    list_filter = ('nome',)
    list_per_page = 10
    search_fields = ('nome', 'sobrenome')
    list_editable = ('mostrar', 'telefone')

admin.site.register(Categoria)
admin.site.register(Contato, ContatoAdmin)

