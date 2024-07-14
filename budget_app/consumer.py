import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import *
from .serializers import *
from channels.db import database_sync_to_async
from channels.exceptions import StopConsumer
import asyncio

class VoucherConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def all_voucher(self):
        voucher = voucherDetail.objects.all()
        voucher_serializer = Voucher_BudgetSerializer(voucher, many=True)
        voucher_data = voucher_serializer.data
        return voucher_data

    async def connect(self):
        self.group_name = 'all_voucher'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        await self.send_voucher_data()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_voucher_data(self):
        voucher = await self.all_voucher()
        await self.send(json.dumps({"voucher": voucher}))

    async def update(self, event):
        event['text']
        await self.send_voucher_data()

class VoucherDetailConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def all_voucher_details(self, voucher_id):
        voucher_details = voucherDetail.objects.filter(id=voucher_id)
        voucher_details_serializer = Voucher_BudgetSerializer(voucher_details, many=True)
        voucher_details_data = voucher_details_serializer.data
        return voucher_details_data

    async def connect(self):
        self.group_name = 'all_voucher_details'
        voucher_id = self.scope['url_route']['kwargs']['voucher_id']
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        await self.send_voucher_details_data(voucher_id)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_voucher_details_data(self, voucher_id):
        voucher_details = await self.all_voucher_details(voucher_id)
        await self.send(json.dumps({"voucher_details": voucher_details}))

    async def update(self, event):
        voucher_id = event['voucher_id']
        await self.send_voucher_details_data(voucher_id)


class DepartmentBudget(AsyncWebsocketConsumer):
    @database_sync_to_async
    def all_budget(self):
        budget = DepartmentBugetDetails.objects.all()
        budget_serializer = DepartmentBudgetSerializer(budget, many=True)
        budget_data = budget_serializer.data
        return budget_data

    async def connect(self):
        self.group_name = 'all_budget'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        await self.send_budget_data()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_budget_data(self):
        budget = await self.all_budget()
        await self.send(json.dumps({"budget": budget}))

    async def update(self, event):
        event['text']
        await self.send_budget_data()
