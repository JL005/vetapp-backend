from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from users.models import Farmer, Veterinarian, User
from users.serializers import FarmerSerializer, VeterinarianSerializer
from django.contrib.auth import authenticate, login, logout
from knox.models import AuthToken
from knox.settings import CONSTANTS


class FarmerList(APIView):
    
    def get(self, request):
        farmers_list = Farmer.objects.all()
        serializer = FarmerSerializer(farmers_list, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FarmerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.check_farmer_exists(serializer.validated_data)
        self.create_farmer(serializer)
        return Response({'response': 'Te has registrado existosamente'}, status=status.HTTP_201_CREATED)
        
    def create_farmer(self, farmer_serializer):
        try:
            farmer_serializer.save()
        except:
            raise serializers.ValidationError({'response':'Ha ocurrido un error al registrarte, intentalo nuevamente más tarde'})
            
    def check_farmer_exists(self, validated_data):
        email = validated_data['email']
        document_number = validated_data['document_number']
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'response':'Ya existe un usuario registrado con este correo'})
        if User.objects.filter(document_number=document_number):
            raise serializers.ValidationError({'response':'Ya existe un usuario registrado con este número de documento'})   

class FarmerDetail(APIView):

    def get_object(self, token):
        user = AuthToken.objects.get(token_key=token[:CONSTANTS.TOKEN_KEY_LENGTH])
        if not user:
            return None
        return user.user

    def get(self, request):
        token  = request.headers['Authorization']
        farmer = self.get_object(token)
        if not farmer:
            return Response({'response': 'No existe un usuario con este token'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = FarmerSerializer(farmer)
        return Response(serializer.data)

    def put(self, request, id):
        pass

    def delete(self, request, id):
        pass

class VeterinarianList(APIView):

    def get(self, request):
        veterinarians_list = Veterinarian.objects.all()
        serializer = VeterinarianSerializer(veterinarians_list, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = VeterinarianSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.check_veterinarian_exists(serializer.validated_data)
        self.create_veterinarian(serializer)
        return Response({'response': 'Te has registrado existosamente'}, status=status.HTTP_201_CREATED)
        
    def create_veterinarian(self, veterinarian_serializer):
        try:
            veterinarian_serializer.save()
        except:
            raise serializers.ValidationError({'response':'Ha ocurrido un error al registrarte, intentalo nuevamente más tarde'})
            
    def check_veterinarian_exists(self, validated_data):
        email = validated_data['email']
        document_number = validated_data['document_number']
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'response':'Ya existe un usuario registrado con este correo'})
        if User.objects.filter(document_number=document_number):
            raise serializers.ValidationError({'response':'Ya existe un usuario registrado con este número de documento'})   
    
class VeterinarianDetail(APIView):
    def get_object(self, id):
        try:
            return Veterinarian.objects.get(id=id)
        except Veterinarian.DoesNotExist:
            raise Http404

    def get(self, request, id):
        veterinarian = self.get_object(id)
        serializer = VeterinarianSerializer(veterinarian)
        return Response(serializer.data)

    def put(self, request, id):
        pass

    def delete(self, request, id):
        pass


class UserDetail(APIView):

    def get_object(self, token):
        user = AuthToken.objects.get(token_key=token[:CONSTANTS.TOKEN_KEY_LENGTH])
        if not user:
            return None
        return user.user

    def get(self, request):
        token  = request.headers['Authorization']
        user = self.get_object(token)
        if not user:
            return Response({'response': 'No estás logueado'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = FarmerSerializer(user)
        return Response(serializer.data)