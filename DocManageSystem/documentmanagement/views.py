from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Doc, Dir
from .serializers import DocSerializer, DirSerializer

@api_view(['GET'])
def dir_list(request):
    dirs = Dir.objects.all()
    serializer = DirSerializer(dirs, many=True)
    # document list, status
    return Response(serializer.data)
        

@api_view(['GET'])
def doc_view(request):
    docs = Doc.objects.all()
    serializer = DocSerializer(docs, many=True)
    # content, status code
    return Response(serializer.data)
        

@api_view(['GET', 'POST'])
def doc_list(request):
    if request.method == 'GET':
        docs = Doc.objects.all()
        serializer = DocSerializer(docs, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = DocSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {"status": "success"}
            return Response(data, status=status.HTTP_201_CREATED)
        data = {"status": "fail"}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def doc_detail(request, pk):
    try:
        doc = Doc.objects.get(pk=pk)
    except Doc.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DocSerializer(doc)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = DocSerializer(doc, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        doc.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

