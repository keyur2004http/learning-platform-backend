from rest_framework.response import Response
from rest_framework.decorators import api_view

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .serializers import RegisterSerializer


@api_view(['POST'])
def register_api(request):
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()

        return Response(
            {
                'message': 'User registered successfully',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                }
            },
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_api(request):
    user = request.user

    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'bio': user.bio,
    })