from rest_framework import status, generics, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from .serializers import BookSerializer
from .utils import APIResponse, api_response
from .constants import (
    SUCCESS_BOOKS_RETRIEVED, NO_BOOKS_TO_LIST, ERROR_CONNECTING_DATABASE,
    SUCCESS_BOOK_CREATED, INVALID_DATA, SUCCESS_BOOK_RETRIEVED,
    SUCCESS_BOOK_UPDATED, SUCCESS_BOOK_DELETED, BOOK_NOT_FOUND
)
from .services import BookService
from .swagger import (
    retrieve_list_schema, create_book_schema,
    retrieve_book_schema, update_book_schema,
    delete_book_schema, average_price_schema
)


class BookListCreateView(generics.ListCreateAPIView):
    """
    get:
    Retrieve a list of books.

    post:
    Create a new book.
    """
    serializer_class = BookSerializer
    pagination_class = PageNumberPagination
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        try:
            return BookService.get_all_books()
        except Exception as e:
            return None

    @retrieve_list_schema
    @api_response(SUCCESS_BOOKS_RETRIEVED, ERROR_CONNECTING_DATABASE)
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset is None:
            raise Exception(ERROR_CONNECTING_DATABASE)

        if not queryset:
            return []

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)
            paginated_data = {
                "count": paginated_response.data['count'],
                "next": paginated_response.data['next'],
                "previous": paginated_response.data['previous'],
                "results": paginated_response.data['results']
            }
            return paginated_data

        serializer = self.get_serializer(queryset, many=True)
        return serializer.data

    @create_book_schema
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                book = BookService.create_book(serializer.validated_data)
                response_serializer = BookSerializer(book)
                return APIResponse(
                    success=True,
                    message=SUCCESS_BOOK_CREATED,
                    data=response_serializer.data,
                    status=status.HTTP_201_CREATED,
                )
            except Exception as e:
                return APIResponse(
                    success=False,
                    message=ERROR_CONNECTING_DATABASE,
                    data=[],
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        missing_fields = [field for field in serializer.errors]
        missing_fields_message = "Todos los campos son obligatorios: {} " \
                                 "son necesarios.".format(", ".join(missing_fields))
        return APIResponse(
            success=False,
            message=missing_fields_message,
            data=[],
            status=status.HTTP_400_BAD_REQUEST,
        )


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update, or delete a book by ID.
    """
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        book_id = self.kwargs.get('pk')
        try:
            return BookService.get_book_by_id(book_id)
        except NotFound:
            raise
        except Exception as e:
            raise Exception(ERROR_CONNECTING_DATABASE)

    @retrieve_book_schema
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return APIResponse(
                success=True,
                message=SUCCESS_BOOK_RETRIEVED,
                data=serializer.data,
                status=status.HTTP_200_OK,
            )
        except NotFound:
            return APIResponse(
                success=False,
                message=BOOK_NOT_FOUND,
                data=[],
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return APIResponse(
                success=False,
                message=str(e),
                data=[],
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @update_book_schema
    def put(self, request, *args, **kwargs):
        book_id = self.kwargs.get('pk')
        try:
            book = self.get_object()
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                updated_book = BookService.update_book(book_id, serializer.validated_data)
                response_serializer = BookSerializer(updated_book)
                return APIResponse(
                    success=True,
                    message=SUCCESS_BOOK_UPDATED,
                    data=response_serializer.data,
                    status=status.HTTP_200_OK,
                )
            return APIResponse(
                success=False,
                message=INVALID_DATA,
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        except NotFound:
            return APIResponse(
                success=False,
                message=BOOK_NOT_FOUND,
                data=[],
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return APIResponse(
                success=False,
                message=ERROR_CONNECTING_DATABASE,
                data=[],
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @delete_book_schema
    def delete(self, request, *args, **kwargs):
        book_id = self.kwargs.get('pk')
        try:
            book = self.get_object()
            BookService.delete_book(book_id)
            return APIResponse(
                success=True,
                message=SUCCESS_BOOK_DELETED,
                data=[],
                status=status.HTTP_204_NO_CONTENT,
            )
        except NotFound:
            return APIResponse(
                success=False,
                message=BOOK_NOT_FOUND,
                data=[],
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return APIResponse(
                success=False,
                message=ERROR_CONNECTING_DATABASE,
                data=[],
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class AveragePriceView(APIView):
    """
    View to get the average price of books published in a specific year.
    """
    permission_classes = [permissions.IsAuthenticated]

    @average_price_schema
    def get(self, request, year, *args, **kwargs):
        try:
            average_price = BookService.get_average_price_by_year(year)
            return APIResponse(
                success=True,
                message=f"Average price for books published in {year}",
                data={"average_price": average_price},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return APIResponse(
                success=False,
                message=ERROR_CONNECTING_DATABASE,
                data=[],
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
