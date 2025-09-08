from datetime import datetime
from enum import verify

from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .serializers import SignUpSerializer,ChangeInfoUserSerializer
from .models import CustomUser, NEW, CODE_VERIFIED, VIA_PHONE, VIA_EMAIL
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.generics import ListCreateAPIView,UpdateAPIView
from rest_framework.views import APIView

class SignupView(ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]


class VerifyCodeApiView(APIView):
    permission_classes = [IsAuthenticated,]

    def post(self,request,*args,**kwargs):
        code=self.request.data.get('code')
        user=self.request.user


        self.check_verify(user,code)
        data={
            'success': True,
            'code_status':True,
            'auth_status':user.auth_status,
            'access_token':user.token()['access'],
            'refresh_token':user.token()['refresh_token']
        }
        return Response(data=data,status=status.HTTP_200_OK)

    @staticmethod
    def check_verify(user,code):
        verify=user.verify_codes.filter(code=code,code_status=False,expiration_time__gte=datetime.now())
        if not verify.exists():
            data={
                'success':False,
                'msg':'Kodingiz eskirgan yoki hato!'
            }
            raise ValidationError(data)
        else:
            verify.code_status=True
        if user.auth_status==NEW:
            user.auth_status=CODE_VERIFIED
            user.save()


class GetNewCodeVerify(APIView):
    def get(self,request,*args,**kwargs):
        user=self.request.user


        self.check_verification(user)
        if user.auth_type==VIA_PHONE:
            code=user.create_verify_code(VIA_PHONE)
            print(f"VIA_PHONE CODE:{code}")
        elif user.auth_type == VIA_EMAIL:
            code = user.create_verify_code(VIA_EMAIL)
            print(f"VIA_EMAIL CODE:{code}")
        else:
            raise ValidationError({'msg':'Telefon yoki email hato'})
        data={
            'status':status.HTTP_200_OK,
            'mdg':'Kod email/phone ga jonatildi',
            'access_token': user.token()['access'],
            'refresh_token': user.token()['refresh_token']
        }
        return Response(data)
    @staticmethod
    def check_verification(user):
        verify=user.verify_codes.filter(expiration_time__gte=datetime.now(),code_status=False)
        if verify:
            data={
                'msg':'Sizda aktiv kod bor ,Shu kodan foydalaning',
                'status':status.HTTP_400_BAD_REQUEST
            }
            raise ValidationError(data)
        return True



class  ChangeInfoUserApi(UpdateAPIView):
    serializer_class = ChangeInfoUserSerializer
    http_method_names = ['PUT','PATCH']
    def get_object(self):
        return self.request.user
    def update(self, request, *args, **kwargs):
        super(ChangeInfoUserApi,self).update(request,*args,**kwargs)
        data = {
            'msg': 'Malumotlar yangilandi',
            'status': status.HTTP_200_OK
        }
        return Response(data)

    def partial_update(self, request, *args, **kwargs):
        super(ChangeInfoUserApi,self).partial_update(*args,**kwargs)
        data={
            'msg':'Malumotlar yangilandi',
            'status':status.HTTP_200_OK
        }
        return Response(data)


