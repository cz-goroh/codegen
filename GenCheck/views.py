from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import uuid, json
from uuid import uuid4


class CheckCode(APIView):
    def get(self, request):
        try:
            fl = open('groups.json')
            groups_dict = json.load(fl)
            for gr_nm, uid_list in groups_dict.items():
                if request.query_params.get('key', None) in uid_list:
                    return Response({'is_exists': True, 'group': gr_nm})
        except:
            pass

        return Response({'is_exists': False})

class GenerateView(APIView):
    permission_classes = (IsAuthenticated, )
    def post(self, request):
        try:
            fl = open('groups.json')
            groups_dict = json.load(fl)
        except:
            fl = open('groups.json', 'w')
            groups_dict = {}

        fl.close()
        fl = open('groups.json', 'w')
        for amt in json.loads(request.body):
            if amt['group'] not in groups_dict:
                groups_dict[amt['group']] = [str(uuid4()) for i in range(int(amt['amount']))]
            else:
                for i in range(int(amt['amount'])):
                    groups_dict[amt['group']].append(str(uuid4()))
        # print(groups_dict)
        json.dump(groups_dict, fl)
        # fl.write('hi')
        fl.close()
        return Response({'result':'ok', 'groups_dict': groups_dict})


class Logout(APIView):
    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
