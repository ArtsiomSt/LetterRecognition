from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from converter.settings import BASE_DIR

from .functions_for_images.funcs_for_rec import get_letters_from_picture, array_of_letters_to_str, get_text_from_picture
from .serializers import PictureAPISerializer


class RecognisePictureAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        return Response({'answer': "This url is supposed to be giver a picture for recognising text from it. Send picture using POST."})

    def post(self, request, format=None):
        serializer = PictureAPISerializer(data=request.data)
        base_dir = str(BASE_DIR)
        if serializer.is_valid():
            new_picture = serializer.save()
            path_to_img = base_dir + new_picture.image.url
            byte_encode, recognised_letters = get_text_from_picture(path_to_img)
            return Response({'letters': recognised_letters, 'new_img': byte_encode})
        return Response({'answer': 'error'})
