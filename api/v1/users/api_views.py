from .serializers import StreamLabsSerializer
from donation.utils import get_access_token, get_user
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.db import transaction

User = get_user_model()


class RegisterUserView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = StreamLabsSerializer

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def post(self, request, *args, **kwargs):
        serializer = StreamLabsSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                with transaction.atomic():
                    access_token = get_access_token(serializer.validated_data['code'])
                    streamlabs_user = get_user(access_token=access_token)
                    sl_data = streamlabs_user.get('streamlabs', {})
                    username = sl_data.get('username')


                    user, created = User.objects.get_or_create(
                        defaults={
                            'email': f"{username}@streamlabs.user",
                            'first_name': sl_data.get('display_name', '').split()[0],
                            'last_name': ' '.join(sl_data.get('display_name', '').split()[1:]),
                            'is_active': True,
                            'streamlabs_token': access_token
                        }
                    )

                    if not created:
                        user.streamlabs_token = access_token
                        user.save()

                    # Generate JWT tokens
                    tokens = self.get_tokens_for_user(user)

                    return Response({
                        **tokens,  # Include refresh and access tokens
                        'user': {
                            'id': user.id,
                            'email': user.email,
                            'streamlabs_id': sl_data.get('id'),
                            'streamlabs_token': access_token
                        },
                        'created': created
                    }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

            except Exception as e:
                return Response({
                    'error': str(e),
                    'message': 'Failed to register user'
                }, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)