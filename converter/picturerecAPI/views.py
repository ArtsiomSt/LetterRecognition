import cv2
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
import cv2
import numpy as np
from PIL import Image
import pickle


class RecognisePictureAPIView(APIView):
    def get(self, request):
        return Response({'answer': "This url is supposed to be giver a picture for recognising text from it. Send picture using POST."})

    def post(self, request):
        file = request.FILES['files']
        img = pickle.load(file)
        print(img)
        object = np.asarray(img, dtype='uint8')
        print(object)
        print(object.dtype)
        cv2.imshow('r', object)
        cv2.waitKey(0)
#        image_stream = file.file
#        f = image_stream.read()
#        image = np.asarray(f)
#        img = Image.open(image_stream)
#        cv2.imwrite('nex.png', image)
#        print(image.__class__)
#        cv2.imshow('t', img)
#        cv2.waitKey(0)
        return Response({'answer': 'success'})
# Create your views here.
