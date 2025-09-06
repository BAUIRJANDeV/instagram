from .serializers import SignupSerializer
from .models import CustomUser
from rest_framework.permissions import AllowAny
from rest_framework.generics import ListCreateAPIView


class SignupView(ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = SignupSerializer
    permission_classes = [AllowAny]


