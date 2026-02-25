from django.shortcuts import render
from django.utils.translation import gettext_lazy as _


def feed(request):
    return render(request, 'feed.html')


def follow_user(request, user_id):
    pass


def comment_post(request, post_id):
    pass


def messages(request):
    message_rows = [
        {'name': 'Samantha Ramirez', 'message': _('Por supuesto'), 'time': '10:07 AM', 'bold': True},
        {'name': 'Gustavo Berne', 'message': _('Tu: OK'), 'time': _('Lun'), 'bold': False},
        {'name': 'Jose Campos', 'message': _('Tu: Creo que deberia cambiarse'), 'time': _('Vie'), 'bold': False},
        {'name': 'Luisdavid Colina', 'message': _('Tu: Luego lo revisare'), 'time': _('Mie'), 'bold': False},
        {'name': 'Gabriel Padilla', 'message': _('Hola, tengo una sugerencia'), 'time': _('Mar'), 'bold': False},
        {'name': 'First Guy', 'message': _('LinkedOut es lo maximo'), 'time': _('Dom'), 'bold': False},
        {'name': 'Second Guy', 'message': _('Tu: OK'), 'time': _('Dom'), 'bold': False},
        {'name': 'Third Guy', 'message': '👍', 'time': _('Oct 9'), 'bold': False},
    ]
    return render(request, 'messages.html', {
        'message_rows': message_rows,
        'page_title': _('Mensajes'),
        'show_bottom_nav': True,
    })


def chat(request, user_id):
    return render(request, 'chat.html')
