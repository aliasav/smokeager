#### This module contains of all mvp APIs ####

from django.contrib.auth.models import User
from django.contrib.sites.models import RequestSite, Site
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.conf import settings

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status

from smoker.models import Smoker, SmokeGroup, SmokeAnalytic, Smoke
from smoker.parser_utils import get_request_content
from smoker.utils import last_smoke, get_user_smoker_from_token, fetch_smoker_analytics, longest_break, \
                            create_smoke_group
from smoker import serializers as smoker_serializers

import logging, json, ast

logger = logging.getLogger(__name__)


@api_view(['POST'])
def signup(request):
    """
    Creates user and smoker object
    """
    logger.debug("Signup api called!")

    valid_data, data = get_request_content("signup", request, smoker_serializers.SignUpSerializer)

    if valid_data:
        logger.debug("Valid data: %s" %data)

        # create user
        try:
            user, created = User.objects.get_or_create(email=data["email"])
        except:
            logger.exception("Error in user object creation: %s" %data)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            # get associated smoker object
            try:
                smoker = user.smoker
            except:
                logger.exception("Error in fetching associated smoker for user: %s" %user)
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:

                if created:
                    user.first_name = data["email"]
                    user.password = data["password"]
                    user.username = data["email"]
                    user.save()

                    smoker.email = data["email"]
                    smoker.name = data["name"]
                    smoker.save()

                    #fetch token
                    t = Token.objects.get(user=user).key

                    logger.debug("New smoker created: %s" %smoker)
                    return Response(status=status.HTTP_200_OK, data={"key": t})

                else:

                    logger.debug("User already exists: %s" %user)
                    return Response(status=status.HTTP_400_BAD_REQUEST)

    # invalid/incomplete data in request
    else:
        logger.debug("Invalid data in response: %s" %data)
        return Response(status=status.HTTP_400_BAD_REQUEST) 



@api_view(['POST'])
def increment_smoke(request):

    """
    Creates smoke object: logs a smoke for smoker(s) and/or smoker_object
    """

    valid_data, data = get_request_content("create_smoke", request, None, ["token_list", "count"])

    if valid_data:

        data["token_list"] = ast.literal_eval(data["token_list"])
        
        # individual smokers
        for token in data["token_list"]:
            try:
                (user, smoker) = get_user_smoker_from_token(token) 
                logger.debug("smoker: %s\tuser: %s" %(user, smoker))
            except:
                logger.exception("Smoker not found for token: %s" %token)

            else:
                # create smoke object
                smoke_obj = Smoke.objects.create()
                smoke_obj.smokers.add(smoker)                
                logger.debug("smoke obj created: %s" %smoke_obj)
                
                # update analytics obj
                try:
                    analytics_obj = smoker.smoke_analytic_individual
                except:
                    logger.exception("Smoker analytic object not found for smoker: %s" %smoker)
                else:
                    logger.debug("Smoke analytic: %s" %analytics_obj)
                    analytics_obj.smoke_count += 1
                    analytics_obj.daily_count += 1
                    analytics_obj.weekly_count += 1
                    analytics_obj.monthly_count += 1
                    analytics_obj.save()
        
        return Response(status=status.HTTP_200_OK)
    
    else:

        return Response(status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def get_stats(request):
    """
    Returns smoke analytics for individual smoker
    """
    resp_data = {}
    valid_data, data = get_request_content("get_stats", request, None, ["token"])

    if valid_data:
        try:
            token = data["token"]
            (user, smoker) = get_user_smoker_from_token(token)
        except:
            logger.exception("Smoker not found: %s" %token)
        else:
            resp_data = fetch_smoker_analytics(user=user)
            logger.debug("stats: %s" %resp_data)
            return Response(status=status.HTTP_200_OK, data=resp_data)
    else:

        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    """
    Login api for user
    """
    resp_data = {}
    valid_data, data = get_request_content("login_api", request, None, ["email", "password"])

    if valid_data:
        try:
            user = User.objects.get(email=data['email'])
        except:
            logger.error("User not found: %s" %data["email"])
        else:
            # check password
            if (user.check_password(data["password"])):
                logger.debug("User successfullly logged in: %s" %data["email"])
                resp_data = fetch_smoker_analytics(user=user)

                if resp_data:
                    return Response(data=resp_data, status=status.HTTP_200_OK)
                else:
                    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # wrong password
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_group(request):
    """
    Creates smoking group and adds users
    """
    resp_data = {}
    valid_data, data = get_request_content("create_group", request, None, ["group_name", "group_password", "token"])

    if valid_data:
        # check existing groups with for same name
        group = SmokeGroup.objects.filter(name=data["group_name"])

        if (len(group)>0):
            resp_data["resp"] = "Group name already exists, try entering a different name!"
            return Response(data=resp_data, status=status.HTTP_409_CONFLICT)
        else:
            smoke_group = create_smoke_group(data)
            if smoke_group:
                resp_data = {
                    "group_name": smoke_group.name,
                    "resp": "Smoke group created successfully!",
                }
                return Response(data=resp_data, status=status.HTTP_200_OK)

            else:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def add_to_group(request):
    """
    Adds a user to a smoke group
    """
    resp_data = {}
    valid_data, data = get_request_content("add_to_group", request, None, ["group_name", "group_password", "token"])

    if valid_data:
        # get smoker group
        try:
            group = SmokeGroup.objects.get(name=data["group_name"])
        except:
            resp_data["resp"] = "Group name does not exist!"
            return Response(status=status.HTTP_404_NOT_FOUND, data=resp_data)
        else:
            # check password
            if (data["group_password"]==group.password):
                user, smoker = get_user_smoker_from_token(data["token"])
                if smoker:
                    group.smokers.add(smoker)
                    group.save()
                    logger.debug("Smoker %s added to group %s." %(smoker, group))
                    return Response(status=status.HTTP_200_OK)

                else:
                    logger.error("Smoker does not exist for token: %s" %data["token"])
                    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            # wrong group password
            else:
                resp_data["resp"] = "Wrong password, try again!"
                return Response(data=resp_data, status=status.HTTP_403_FORBIDDEN)

    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

