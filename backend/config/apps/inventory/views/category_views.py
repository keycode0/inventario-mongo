from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from config.apps.inventory.models.category import Category
from config.apps.inventory.serializers.category_serializer import CategorySerializer
from config.apps.users.permissions.category_permissions import CategoryPermission



class CategoryListCreateView(APIView):
    permission_classes = [CategoryPermission]

    def get(self, request):
        categories = Category.objects(is_active=True)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CategoryDetailView(APIView):
    permission_classes = [CategoryPermission]

    def put(self, request, pk):
        category = Category.objects(id=pk, is_active=True).first()
        if not category:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CategorySerializer(category, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        category = Category.objects(id=pk, is_active=True).first()
        if not category:
            return Response(status=status.HTTP_404_NOT_FOUND)

        category.is_active = False
        category.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
