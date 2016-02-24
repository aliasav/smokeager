from rest_framework import serializers

import json
import logging

logger = logging.getLogger(__name__)

class SignUpSerializer(serializers.Serializer):
    
    email = serializers.EmailField(required=True, allow_blank=False)
    password = serializers.CharField(style={'input_type': 'password'}, required=True, allow_blank=False)    
    name = serializers.CharField(max_length=300, allow_blank=True)

class CreateSmokeSerializer(serializers.Serializer):

    token_list = serializers.ListField()
    count = serializers.IntegerField(min_value=0)