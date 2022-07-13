from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponseNotFound, JsonResponse
from .models import User
from .serializers import UserSerializer
from rest_framework import status
from django.db.models import Q, Value
from django.db.models.functions import Concat

@api_view(['GET'])
def index(request):
    return JsonResponse({
        "/users - GET": "list users params=(page, limit, name, sort)",
        "/api/users - POST": "create new user",
        "/api/users/<id> - GET": "get detail of a user",
        "/api/users - PUT": "update details of a user",
        "/api/users - DELETE": "delete a user"
    }, safe=False)

@api_view(['GET', 'POST'])
def get_all(request):
    if request.method == 'POST':
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
                serializer.save()
                return JsonResponse({}, safe=False)
        else:
            return JsonResponse({"error": serializer.errors}, safe=False, status=400)

    users = User.objects.all()
    page = int(request.GET.get('page', 1))
    limit = int(request.GET.get('limit', 5))
    name = request.GET.get('name', '')
    order_by = request.GET.get('sort', 'id')

    users = users.annotate(full_name=Concat('first_name', Value(' '), 'last_name'))

    users = users.filter(full_name__icontains=name)
    users = users.order_by(order_by)

    total_users = users.count()
    
    if page > (total_users // limit) + 1:
        return JsonResponse({"error": "page is out of bounds"}, status=404, safe=False)
    
    users = users[limit * (page - 1): page * limit]
    
    serializer = UserSerializer(users, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET', 'PUT', 'DELETE'])
def get_user(request, pk):
    try:
        user = User.objects.get(id=pk)
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return JsonResponse(serializer.data, safe=False)
        elif request.method == 'PUT':
            serializer = UserSerializer(data=request.data, instance=user, partial=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({}, safe=False)
            else:
                return JsonResponse({"error": serializer.errors}, safe=False, status=400)
        else:
            user.delete()
            return JsonResponse({}, safe=False)
    except:
        return JsonResponse({"error": "Not Found"}, status=404, safe=False)