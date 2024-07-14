from django.shortcuts import render, redirect
from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import *
from django.contrib.auth.tokens import default_token_generator
# from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib import messages
import requests
from .forms import *
from django.conf import settings
from rest_framework import generics
from django.core.mail import send_mail
from django.http import JsonResponse


domain = 'http://' + settings.DOMAIN
password_token = settings.CUSTOM_PASSWORD_TOKEN
email_host = settings.EMAIL_HOST_USER
############################ DEPARMTENT #################################3


class DepartmentListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):

        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)

class GetDepartmentDetailsView(APIView):
    # permission_classes = [AllowAny]

    def get(self, request, pk):
        department_details = Department.objects.get(id=pk)
        serializer = DepartmentSerializer(department_details)
        return Response(serializer.data)

class CreateDepartmentView(APIView):
    # permission_classes = [AllowAny]

    def post(self, request):
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class UpdateDepartmentView(APIView):
    # permission_classes = [AllowAny]

    def put(self, request, pk):
        try:
            department_details = Department.objects.get(id=pk)
        except Department.DoesNotExist:
            return Response({"message": "Department not found"}, status=404)

        serializer = DepartmentSerializer(department_details, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

class DeleteDepartentView(APIView):
    # permission_classes = [AllowAny]

    def delete(self, request, pk):
        try:
            department_details = Department.objects.get(id=pk)
        except Department.DoesNotExist:
            return Response({"message": "Department not found"}, status=404)

        department_details.delete()
        return Response({"message": "Department deleted"}, status=204)

############################ EMPLOYEE CODE #################################3
    
class EmployeeCodeListView(APIView):
    # permission_classes = [AllowAny]

    def get(self, request):
        employee_code = EmplyeeCode.objects.all()
        serializer = EmplyeeCodeSerializer(employee_code, many=True)
        return Response(serializer.data)

class GetEmployeeCodeDetailsView(APIView):
    # permission_classes = [AllowAny]

    def get(self, request, pk):
        employee_code = EmplyeeCode.objects.get(id=pk)
        serializer = DepartmentSerializer(employee_code)
        return Response(serializer.data)

class CreateEmployeeCodeView(APIView):
    # permission_classes = [AllowAny]

    def post(self, request):
        serializer = EmplyeeCodeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class UpdateEmployeeCodeView(APIView):
    # permission_classes = [AllowAny]

    def put(self, request, pk):
        try:
            employee_code = EmplyeeCode.objects.get(id=pk)
        except EmplyeeCode.DoesNotExist:
            return Response({"message": "Department not found"}, status=404)

        serializer = EmplyeeCodeSerializer(employee_code, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

class DeleteEmployeeCodeView(APIView):
    permission_classes = [AllowAny]

    def delete(self, request, pk):
        try:
            employee_code = EmplyeeCode.objects.get(id=pk)
        except EmplyeeCode.DoesNotExist:
            return Response({"message": "Department not found"}, status=404)

        employee_code.delete()
        return Response({"message": "Department deleted"}, status=204)
    
############################ activate account ####################################

def activate_account(request, uid, token):
    # permission_classes = [AllowAny]

    try:
        if uid and token:
            # Convert uid and token to JSON string

            uid =str(uid)
            token = str(token)
            data = {'uid': uid, 'token': token}

            # Make a POST request to the activation API
            activation_url = f'{domain}/{password_token}/auth/users/activation/'
            response = requests.post(activation_url, data=data)

            # Check if activation was successful

            message = 'Your account has been activated successfully. You can now log into the app.'

        else:
            message = 'Invalid activation link.'
    except User.DoesNotExist:
        message = 'Invalid activation link: User does not exist.'

    return render(request, 'activate.html', {'message': message})

def reset_email(request, uid, token):
    # Check if the request method is POST
    message = ''
    email_ = ''
    email_re = ''
    token = ''
    
    if request.method == 'POST':
        form = EmailResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            re_email = form.cleaned_data['re_email']

            # Ensure the email and re_email match
            if email == re_email:
                try:
                    if uid and token:
                        # Convert uid and token to strings
                        uid = str(uid)
                        token = str(token)
                        
                        # Construct data for the activation request
                        data = {'uid': uid, 'token': token, 'new_email': email, 're_new_email': re_email}

                        # Make a POST request to the activation API
                        activation_url = f'{domain}/{password_token}/auth/users/reset_email_confirm/'
                        response = requests.post(activation_url, data=data)

                        # Check if the activation was successful
                        if response.status_code == 204:
                            message = 'Email reset successfully.'
                        else:
                            response_data = response.json()

                            if 'new_email' in response_data:
                                email_ = response_data['new_email']
                            else:
                                email_ = ''

                            if 're_new_email' in response_data:
                                email_re = response_data['re_new_email']
                            else:
                                email_re = ''

                            if 'token' in response_data:
                                token = response_data['token']
                            else:
                                token = ''
                            
                    else:
                        message = 'Invalid activation link.'
                except User.DoesNotExist:
                    message = 'Invalid activation link: User does not exist.'
            else:
                message = 'Email and confirmation email do not match.'
        else:
            message = 'Form is not valid.'
    else:
        form = EmailResetForm()  # Instantiate the form for GET requests

    # Render the template with the message and form
    return render(request, 'reset_email.html', {'form': form, 'message': message, 'email_': email_, 'email_re': email_re, 'token':token})



def reset_password(request, uid, token):
    message = ''
    password_ = ''  # Initialize password_ variable
    token = ''

    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            re_password = form.cleaned_data['re_password']
            
            # Check if passwords match
            if password == re_password:
                try:
                    if uid and token:
                        uid = str(uid)
                        token = str(token)
                        data = {'uid': uid, 'token': token, 'new_password': password, 're_new_password': re_password}

                        activation_url = f'{domain}/{password_token}/auth/users/reset_password_confirm/'
                        response = requests.post(activation_url, data=data)

                        # Check if activation was successful
                        if response.status_code == 204:
                            message = 'Password reset successfully.'
                        else:
                            # Parse response content as JSON
                            response_data = response.json()

                            # Extract error message from 'detail' field

                            if 'new_password' in response_data:
                                password_ = response_data['new_password']
                            else:
                                password_ = ''

                            if 'token' in response_data:
                                token = response_data['token']
                            else:
                                token = ''
                    else:
                        message = 'Invalid activation link.'
                except User.DoesNotExist:
                    message = 'Invalid activation link: User does not exist.'
            else:
                message = 'Password and confirmation password do not match.'
        else:
            message = 'Form is not valid.'
            
    else:
        form = PasswordResetForm()

    return render(request, 'reset_password.html', {'form': form, 'message': message, 'password_': password_, 'token': token})



########################### update user info ######################################
class UpdateProfileView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateUserSerializer
    
########################## error handling ###############################33
from django.http import HttpResponseBadRequest, HttpResponseNotFound

def bad_request(request, exception):
    return HttpResponseBadRequest(render(request, 'error.html'))

def page_not_found(request, exception):
    return HttpResponseNotFound(render(request, 'error.html'))


############### update email ##############################################333
# def reset_username_view(request):
#     # Logic to generate reset link and send email
#     # Example logic:
#     reset_link = f'https://{domain}/reset_username_link'  # Replace with your actual reset link
#     user_email = f''  # Example user email

#     send_mail(
#         'Reset Your Username',
#         f'Click the link to reset your username: {reset_link}',
#         settings.DEFAULT_FROM_EMAIL,
#         email_host,
#         fail_silently=False,
#     )

#     return JsonResponse({'message': 'Reset link sent successfully'})