from .functions_for_images.funcs_for_rec import get_letters_from_picture, array_of_letters_to_str
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ImageSerializer, PictureAPISerializer
from .models import PictureForRecognising
from converter.settings import BASE_DIR
import os
import cv2
import numpy as np
import json
import base64


class RecognisePictureAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        return Response({'answer': "This url is supposed to be giver a picture for recognising text from it. Send picture using POST."})

    def post(self, request, format=None):
        print(request.data)
        serializer = PictureAPISerializer(data=request.data)
        base_dir = str(BASE_DIR)
        if serializer.is_valid():
            new_picture = serializer.save()
            path_to_img = base_dir + new_picture.image.url.replace('/', '\\')
            img = cv2.imread(path_to_img)
            letters, rectangled_img = get_letters_from_picture(img)
            recognised_letters = array_of_letters_to_str(letters)
            img_encode = cv2.imencode('.png', rectangled_img)[1]
            data_encode = np.array(img_encode)
            byte_encode = data_encode.tobytes()
            c = base64.b64encode(byte_encode)
            print(base64.b64encode(byte_encode))
            print(base64.b64decode(c).__class__)
            return Response({'letters': recognised_letters, 'new_img': base64.b64encode(byte_encode)})
        return Response({'answer': 'success'})
