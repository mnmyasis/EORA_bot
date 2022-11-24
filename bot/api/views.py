from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import MessageSerializer


class MessageView(APIView):

    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        serializer.is_valid()
        question = serializer.save()
        context = {}
        if question:
            context['text'] = question.text
        else:
            context['text'] = None
        return Response(context)
