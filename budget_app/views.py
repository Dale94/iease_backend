import asyncio
from django.shortcuts import render
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import *
from rest_framework.permissions import IsAuthenticated
from channels.generic.websocket import WebsocketConsumer
from accounts.models import *
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .utils import *


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetVoucherListView(request):
    que_details = voucherDetail.objects.all()
    serializers = Voucher_BudgetSerializer(que_details, many=True)
    return Response(serializers.data)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetVoucherDetailsView(request, pk):
    que_details = voucherDetail.objects.get(id=pk)
    serializers = Voucher_BudgetSerializer(que_details, many=False)
    return Response(serializers.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def CreateVoucherView(request, pk):
    data = request.data

    department_detail = Department.objects.get(pk=pk)

    que_details = voucherDetail.objects.create(
        user_name=data['user_name'],
        department=department_detail,
        voucher_code=data['voucher_code'],
        details=data['details'],
        amount=data['amount'],
        accounting_approval=False,
        mayor_approval=False,
        treasury_approval=False,
    )
    serializer = Voucher_BudgetSerializer(que_details, many=False)
    send_voucher_update()
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def AprroveAccoutingView(request, pk):

    que_details = voucherDetail.objects.get(id=pk)
    serializer = Voucher_AccountingSerializer(que_details, data=request.data)

    if serializer.is_valid():
        serializer.save()
        send_voucher_details_update(pk)
        # print(request.data)

    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def AprroveMayorView(request, pk):

    que_details = voucherDetail.objects.get(id=pk)
    serializer = Voucher_MayorSerializer(que_details, data=request.data)

    if serializer.is_valid():
        serializer.save()
        send_voucher_details_update(pk)

        # print(request.data)

    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def AprroveTreasuryView(request, pk):

    que_details = voucherDetail.objects.get(id=pk)
    serializer = Voucher_TreasurySerializer(que_details, data=request.data)

    if serializer.is_valid():
        serializer.save()
        send_voucher_details_update(pk)

        # print(request.data)

    return Response(serializer.data)


####################### budget ######################3

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def CreateBudgetView(request, pk):
    data = request.data

    department_detail = Department.objects.get(pk=pk)

    budget_details = DepartmentBugetDetails.objects.create(
        department=department_detail,
        added_budget=data['added_budget'],
    )
    serializer = DepartmentBudgetSerializer(budget_details, many=False)
    send_budget_update()
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetDepartmentBudgetListView(request):
    que_details = DepartmentBugetDetails.objects.all()
    serializers = DepartmentBudgetSerializer(que_details, many=True)
    return Response(serializers.data)