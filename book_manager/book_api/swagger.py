from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .serializers import BookSerializer

retrieve_list_schema = swagger_auto_schema(
    operation_description="Retrieve a list of books.",
    responses={200: openapi.Response('List of books', BookSerializer(many=True))}
)

create_book_schema = swagger_auto_schema(
    operation_description="Create a new book.",
    request_body=BookSerializer,
    responses={201: openapi.Response('Book created', BookSerializer)}
)

retrieve_book_schema = swagger_auto_schema(
    operation_description="Retrieve a book by ID.",
    responses={200: openapi.Response('Book details', BookSerializer)}
)

update_book_schema = swagger_auto_schema(
    operation_description="Update a book by ID.",
    request_body=BookSerializer,
    responses={200: openapi.Response('Book updated', BookSerializer)}
)

delete_book_schema = swagger_auto_schema(
    operation_description="Delete a book by ID.",
    responses={204: openapi.Response('Book deleted')}
)

average_price_schema = swagger_auto_schema(
    operation_description="Get the average price of books published in a specific year.",
    responses={200: openapi.Response('Average price', openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'average_price': openapi.Schema(type=openapi.TYPE_NUMBER, description='Average price of books')
        }
    ))}
)
