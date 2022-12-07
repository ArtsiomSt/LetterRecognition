from .functions_for_images.funcs_for_rec import get_letters_from_picture, array_of_letters_to_str
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ImageSerializer, PictureAPISerializer
from .models import PictureForRecognising
from converter.settings import BASE_DIR
import os
import cv2



class RecognisePictureAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        return Response({'answer': "This url is supposed to be giver a picture for recognising text from it. Send picture using POST."})

    def post(self, request, format=None):
        serializer = PictureAPISerializer(data=request.data)
        base_dir = str(BASE_DIR)
        if serializer.is_valid():
            new_picture = serializer.save()
            path_to_img = base_dir + new_picture.image.url.replace('/', '\\')
            img = cv2.imread(path_to_img)
            letters, rectangled_img = get_letters_from_picture(img)
            recognised_letters = array_of_letters_to_str(letters)
            print(recognised_letters)
            return Response({'letters': recognised_letters, 'newimg': img})
        return Response({'answer': 'success'})



