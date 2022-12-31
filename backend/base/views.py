from django.shortcuts import render
from .serializers import UserSerializerWithToken, imgSerializer
from rest_framework.response import Response
# Create your views here.
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view
from PIL import Image, ImageOps
from .models import Pic


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['POST'])
def upload_img(request):
    original = request.FILES['img']

    data = Pic.objects.create(
        image=original,
        name=original.name,


    )

    data.save()
    output = Pic.objects.get(name=original.name)
    serializer = imgSerializer(output, many=False)

    return Response(serializer.data)
