
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,permissions
from .models import Task
from .serializer import TaskSerializer
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404


class TaskCreateView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def post(self,request):
        serializer=TaskSerializer(data=request.data) 
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"message":"Task created successfully","data":serializer.data }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class TaskListView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def get(self,request):
        tasks=Task.objects.filter(user=request.user)
       
        
        #status
        status_param=request.query_params.get('status')
        if status_param:
           tasks=tasks.filter(status=status_param)
           
        #search
        search=request.query_params.get('search')
        if search:
            tasks=tasks.filter(title__icontains=search)
        
        #pagination
        paginator=PageNumberPagination()
        paginator.page_size=5
        
        result=paginator.paginate_queryset(tasks,request)
        serializer=TaskSerializer(result,many=True)
        return paginator.get_paginated_response(serializer.data)
    
class TaskDetailView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    
    def get(self,request,pk):
        task=get_object_or_404(Task,id=pk,user=request.user)
        serializer=TaskSerializer(task)
        return Response({"message":"This is task details","data":serializer.data})
    
    
class TaskUpdateView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def put(self,request,pk):
        task=get_object_or_404(Task,id=pk,user=request.user)
        serializer=TaskSerializer(task,data=request.data)
        if serializer.is_valid():
              serializer.save()
              return Response({"message":"Task updated","data":serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors,status=400)
    
        
        
class TaskDeleteView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def delete(self,request,pk):
        task=get_object_or_404(Task,id=pk,user=request.user)
        task.delete()
        return Response({"message":"Task successfully deleted"},status=status.HTTP_200_OK)     
                        
