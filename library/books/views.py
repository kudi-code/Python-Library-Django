# Django rest Framework ViewSets 
from rest_framework import  viewsets

# Models
from .models import Book, BookItem

# Permissions
from .permissions import IsLibraryUser, IsRentForAnother

# Serializers
from .serializers import BookSerializer, BookItemSerializer, BookItemCreateSerializer

#Response
from rest_framework import  status
from rest_framework.response import Response

# Searches
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

# Viewsets init Here:

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = [
        "ISBN",
        "title",
        "author",
        "subject"
        "publisher",
        "description"
        "language",
        "numberOfPages"
    ]
    search_fields = {
        "ISBN",
        "title",
        "author",
        "subject"
        "publisher",
        "description"
        "language",
        "numberOfPages"
    }

class BookItemViewSet(viewsets.ModelViewSet):
    queryset = BookItem.objects.all()
    serializer_class = BookItemSerializer
    permission_classes = [IsLibraryUser]

    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = [
        "member"
    ]
    search_fields = {
        "member"
    }

    def get_serializer_class(self):
        if self.action == "create" or self.action == "update":
            return BookItemCreateSerializer
        else:
            return  BookItemSerializer

    def get_permissions(self):
        if self.action ==  "update":
            permissions = [IsRentForAnother]
            return [permission() for permission in permissions]
        else:
            return [IsLibraryUser()]

    def update(self, request, *args, **kwargs):
        totalBooks = 6
        if self.action == "update":
            if self.request.user.is_staff:
                partial = kwargs.pop('partial', False)
                instance = self.get_object()
                if request.data["member"]:
                    books_items = BookItem.objects.filter(member=request.data["member"])
                    total = books_items.count()
                    if total >= totalBooks:
                        return Response({"message": f"No puedes tener mas de {totalBooks} libros"}, status=status.HTTP_400_BAD_REQUEST)
                serializer = self.get_serializer(instance, data=request.data, partial=partial)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)

                if getattr(instance, '_prefetched_objects_cache', None):
                    # If 'prefetch_related' has been applied to a queryset, we need to
                    # forcibly invalidate the prefetch cache on the instance.
                    instance._prefetched_objects_cache = {}

                return Response(serializer.data)
            else:
                partial = kwargs.pop('partial', False)
                instance = self.get_object()
                data = {
                    "is_rent": request.data["is_rent"],
                    "member": request.data["member"]
                }
                if data["is_rent"]:
                    data["is_rent"] = False
                    data["member"] = None
                serializer = self.get_serializer(instance, data=data, partial=True)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)

                if getattr(instance, '_prefetched_objects_cache', None):
                    # If 'prefetch_related' has been applied to a queryset, we need to
                    # forcibly invalidate the prefetch cache on the instance.
                    instance._prefetched_objects_cache = {}

                return Response(serializer.data)


