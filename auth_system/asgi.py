import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from queuing_app.consumers import *
from budget_app.consumer import *

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_system.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter([
        path('ws/queuing/', QueuingConsumer.as_asgi()),
        path('ws/voucher/', VoucherConsumer.as_asgi()),
        path('ws/budget/', DepartmentBudget.as_asgi()),
        path('ws/voucher_details/<int:voucher_id>', VoucherDetailConsumer.as_asgi()),
        path('ws/message/<int:que_id>', MessageConsumer.as_asgi()),
        path('ws/reply/<int:que_id>', RepliesConsumer.as_asgi()), 
    ]),
})
