from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

def send_voucher_update():
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "all_voucher",  # Group name
        {"type": "update", "text": "hellooo"}  # Message
    )

def send_voucher_details_update(voucher_id):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "all_voucher_details",  # Group name
        {"type": "update", "voucher_id": voucher_id}  # Message
    )

def send_budget_update():
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "all_budget",  # Group name
        {"type": "update", "text": "hellooo"}  # Message
    )