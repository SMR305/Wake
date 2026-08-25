from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db import transaction
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Server


def broadcast_server_event(data):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'servers',
        {'type': 'server.event', 'data': data},
    )


def server_data(server):
    return {'name': server.name, 'is_on': server.is_on}


@receiver(post_save, sender=Server)
def server_saved(sender, instance, created, **kwargs):
    event_type = 'server_added' if created else 'server_status'
    transaction.on_commit(lambda: broadcast_server_event({
        'type': event_type,
        'server': server_data(instance),
    }))


@receiver(post_delete, sender=Server)
def server_deleted(sender, instance, **kwargs):
    transaction.on_commit(lambda: broadcast_server_event({
        'type': 'server_removed',
        'name': instance.name,
    }))