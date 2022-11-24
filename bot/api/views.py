from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import MessageSerializer


class MessageView(APIView):

    def post(self, request):
        user_id = request.data.get('user_id')
        message = request.data.get('message')
        serializer = MessageSerializer(data=request.data)
        serializer.is_valid()
        return Response('foo')
