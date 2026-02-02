from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from config.apps.inventory.models.subcategory import SubCategory
from config.apps.inventory.serializers.subcategory_serializer import SubCategorySerializer
from config.apps.users.permissions.subcategory_permissions import SubCategoryPermission


class SubCategoryListCreateView(APIView):
    permission_classes = [SubCategoryPermission]

    def get(self, request):
        queryset = SubCategory.objects(is_active=True)

        category_id = request.query_params.get("category_id")
        if category_id:
            try:
                queryset = queryset.filter(categoria=category_id)
            except Exception:
                return Response(
                    {"detail": "Invalid category_id"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        serializer = SubCategorySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = SubCategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SubCategoryDetailView(APIView):
    permission_classes = [SubCategoryPermission]

    def put(self, request, pk):
        try:
            sub = SubCategory.objects(id=pk, is_active=True).first()
        except Exception:
            return Response(
                {"detail": "Invalid subcategory id"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not sub:
            return Response(
                {"detail": "Subcategory not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = SubCategorySerializer(sub, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            sub = SubCategory.objects(id=pk, is_active=True).first()
        except Exception:
            return Response(
                {"detail": "Invalid subcategory id"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not sub:
            return Response(
                {"detail": "Subcategory not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        sub.is_active = False
        sub.save()
        return Response(
            {"detail": "Subcategory deleted"},
            status=status.HTTP_204_NO_CONTENT,
        )
