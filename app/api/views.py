from django.http import JsonResponse
from rest_framework.decorators import (
  api_view,
  permissions_classes,
)
from rest_framework.permissions import (
  IsAuthenticated,
  IsAdminUser,
)
from rest_framework.response import Response
from .serializers import ProjectSerializer
from projects.models import (
  Project,
  Review,
)
from api import serializers

@api_view(['GET'])
def get_routes(request):
  routes = [
    {'GET': '/api/projects'},
    {'GET': '/api/projects/id'},
    {'POST': '/api/projects/id/vote'},

    {'POST': '/api/users/token'},
    {'POST': '/api/users/token/refresh'},
  ]
  return Response(routes)



# @permissions_classes([IsAuthenticated])
@api_view(['GET'])
def get_projects(request):
  projects = Project.objects.all()
  serializer = ProjectSerializer(projects, many=True)
  return Response(serializer.data)


@api_view(['GET'])
def get_project(request, pk):
  project = Project.objects.all(id=pk)
  serializer = ProjectSerializer(project, many=False)
  return Response(serializer.data)


@api_view(['POST'])
@permissions_classes([IsAuthenticated])
def project_vote(request, pk):
  project = Project.objects.get(id=pk)
  user = request.user.profile
  data = request.data
  review, created =  Review.objects.get_or_create(
    owner=user,
    project=project,
  )
  review.value = data['value']
  review.save()
  project.get_vote_count
  serializer = ProjectSerializer(project, many=False)
  return Response(serializer.data)