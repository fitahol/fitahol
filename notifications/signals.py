from django.dispatch import Signal

notify = Signal(providing_args=[
    'recipient', 'sender', 'action_object', 'title', 'description', 'target', 'show_time'
])
