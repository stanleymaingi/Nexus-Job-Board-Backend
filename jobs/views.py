from rest_framework import generics, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.urls import reverse
from .models import Job, Category, Application
from .serializers import JobSerializer, CategorySerializer, ApplicationSerializer
from django_filters.rest_framework import DjangoFilterBackend




# -----------------------------
# API Root - Public Access
# -----------------------------
@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request, format=None):
    """
    Public API root endpoint listing available resources.
    """
    return Response({
        'jobs': reverse('job-list', request=request, format=format),
        'categories': reverse('category-list', request=request, format=format),
        'applications': reverse('application-list', request=request, format=format),
    })


# -----------------------------
# JOB VIEWS
# -----------------------------
class JobListCreateView(generics.ListCreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class JobDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAuthenticated()]
        return [AllowAny()]


class JobListCreateView(generics.ListCreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['location']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


# -----------------------------
# Category Views
# -----------------------------
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method in ['POST']:
            return [IsAuthenticated()]  # Admin create
        return [AllowAny()]  # Public GET access

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAuthenticated()]  # Admin only
        return [AllowAny()]  # Public GET


# -----------------------------
# Application Views
# -----------------------------


class ApplicationListCreateView(generics.ListCreateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]  # Must be logged in to create
        return [IsAuthenticated()]      # Admin or authenticated user can list

    def perform_create(self, serializer):
        # Automatically set the logged-in user as applicant
        serializer.save(applicant=self.request.user)

class ApplicationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAuthenticated()]  # Admin only
        return [IsAuthenticated()]  # Admin or user can GET


