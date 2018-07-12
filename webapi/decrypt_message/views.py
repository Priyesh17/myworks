# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from decrypt_message.gpg_decriptor import gpgDecrypt


# Create your views here.

@csrf_exempt
@api_view(['POST'])
def decrypt_message(request):
    
    decryption_serializer = gpgDecrypt(data=request.data)
    
    if decryption_serializer.is_valid():
        decrypted_data = decryption_serializer.decrypt()
        return Response({"DecryptedMessage": str(decrypted_data)}, status=status.HTTP_200_OK)
    else:
        error_details = []
        for error in decryption_serializer.errors:
            error_details.append(error)
            
        data = {"Error": {
                    "status": 400,
                    "message": "Invalid data.",
                    "error_details": error_details
                    }
                }

        return Response(data, status=status.HTTP_400_BAD_REQUEST)