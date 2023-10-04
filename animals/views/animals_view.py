from helpers.views.auth_farmer_view import AuthFarmerMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from animals.models import Animals
from animals.serializers.animals import AnimalSerializer

class AnimalsFarmer(AuthFarmerMixin, APIView):

    def get(self, request):
        farmer = self.check_authentication(request)
        if not farmer:
            return Response({'response': 'No tienes permiso para esto'}, status=status.HTTP_400_BAD_REQUEST)
        animals = Animals.objects.filter(farmer=farmer.id)
        animal_serializer = AnimalSerializer(animals, many=True)
        return Response(animal_serializer.data)

    def post(self, request):
        farmer = self.check_authentication(request)
        if not farmer:
            return Response({'response': 'No tienes permiso para esto'}, status=status.HTTP_400_BAD_REQUEST)
        request.data['farmer'] = farmer.id
        serializer = AnimalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AnimalDetail(AuthFarmerMixin,APIView):

    def get(self, request, pk):
        farmer = self.get_farmer(request.headers['Authorization'][6:])
        if pk is None:
            return Response({'response': 'El ID del animal es requerido'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            animal = Animals.objects.get(id=pk)
            if animal.farmer.id != farmer.id:
                return Response({'response': 'No tienes permiso para esto'}, status=status.HTTP_400_BAD_REQUEST)
        except Animals.DoesNotExist:    
            return Response({'response': 'No se encontraron razas para la especie especificada'}, status=status.HTTP_404_NOT_FOUND)
        serializer = AnimalSerializer(animal)
        return Response(serializer.data)