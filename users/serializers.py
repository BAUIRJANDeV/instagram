from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import CodeVerified,CustomUser,VIA_EMAIL,VIA_PHONE
from shared.utility import chech_email_or_phone

class SignupSerializer(serializers.ModelSerializer):
    id=serializers.UUIDField(read_only=True)
    auth_type=serializers.CharField(required=False,read_only=True)
    auth_status=serializers.CharField(required=False,read_only=True)

    def __init__(self,*args,**kwargs):
        super(SignupSerializer,self).__init__(*args,**kwargs)
        self.fields['email_phone_number']=serializers.CharField(required=False,read_only=True)

    class Meta:
        model=CustomUser
        fields=['id','auth_type','auth_status']

    def create(self, validated_data):
        user=super(SignupSerializer,self).create(validated_data)
        if user.auth_type==VIA_EMAIL:
            code=user.create_verfiy_code(VIA_EMAIL)
            # send_to_mail(user.email,code)
        elif user.auth_type==VIA_PHONE:
            code=user.create_verfiy_code(VIA_PHONE)
            # send_to_phone(user.phone,code)
            user.save()
            return user




    def validate(self, data):
        super(SignupSerializer,self).validate(data)
        data=self.auth_validate(data)
        return data

    def validate_email_phone_number(self,data):
        if data and CustomUser.objects.filter(email=data).exists():
            raise ValidationError('BU email orqali royhatan otilgan')
        elif data and CustomUser.objects.filter(phone_number=data):
            raise ValidationError('Bu telefon orqali royhatan otilgan')
        return data


    @staticmethod
    def auth_validate(data):
        user_input=str(data.get('email_phone_number')).lower()
        auth_type=chech_email_or_phone(user_input)
        if auth_type=='email':
            data={
                'auth_type':VIA_EMAIL,
                'email':user_input
            }
        elif auth_type=='phone':
            data={
                'auth_type':VIA_PHONE,
                'phone_number':user_input
            }
        else:
            data={
                'success':False,
                'msg':'Siz telfon raqam yoki email kiritishingiz kk edi!'

            }
            raise ValidationError(data)

        return data