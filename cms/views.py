from rest_framework import status, permissions, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CafeCms
from .serializers import CmsSerializer
from cafe.render import UserRenderer


# view to create the cms for the cafe.
class CafeCmsCreateApiView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, format=None):
        serializer = CmsSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            serializer.validated_data["created_by"] = user.username
            serializer.save()
            return Response(
                {
                    "msg": "Cafe Cms created.",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


# view to see the cms of the cafe.
class CafeCmsListApiView(generics.ListAPIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.IsAdminUser]
    queryset = CafeCms.objects.all()
    serializer_class = CmsSerializer


# view to retrive the single cafe cms data.
class CafeCmsDetailApiView(generics.RetrieveAPIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.IsAdminUser]
    serializer_class = CmsSerializer

    def get_object(self):
        id = self.kwargs.get("pk")
        return CafeCms.objects.get(id=id)


# view to delete the cafe cms.
class CafeCmsDeleteApiView(generics.DestroyAPIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.IsAdminUser]
    queryset = CafeCms.objects.all()
    serializer_class = CmsSerializer


# view to update the cafe cms.
class CafeCmsUpdateApiView(generics.UpdateAPIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.IsAdminUser]
    queryset = CafeCms.objects.all()
    serializer_class = CmsSerializer

    def perform_update(self, serializer):
        user = self.request.user
        serializer.save(updated_by=user.username)
