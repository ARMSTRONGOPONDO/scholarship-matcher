from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions, status

from ..models import Resource, Disorder, Therapist
from ..serializers import ResourceSerializer, DisorderSerializer, TherapistSerializer

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def search(request):
    query = request.query_params.get('q', '')
    if not query:
        return Response({"error": "Query parameter 'q' is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    # Search in resources
    resources = Resource.objects.filter(title__icontains=query) | Resource.objects.filter(description__icontains=query)
    resource_serializer = ResourceSerializer(resources, many=True)
    
    # Search in disorders
    disorders = Disorder.objects.filter(name__icontains=query) | Disorder.objects.filter(description__icontains=query)
    disorder_serializer = DisorderSerializer(disorders, many=True)
    
    # Search in therapists
    therapists = Therapist.objects.filter(name__icontains=query) | Therapist.objects.filter(bio__icontains=query)
    therapist_serializer = TherapistSerializer(therapists, many=True)
    
    return Response({
        "resources": resource_serializer.data,
        "disorders": disorder_serializer.data,
        "therapists": therapist_serializer.data
    })
