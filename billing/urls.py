# from django.urls import path
# from .views import BillingListCreateView, BillingDetailView

# urlpatterns = [
#     path('billing/', BillingListCreateView.as_view(), name='billing-list-create'),
#     path('billing/<int:pk>/', BillingDetailView.as_view(), name='billing-detail'),
# ]


from django.urls import path
from .views import BillingListCreateView, BillingDetailView

urlpatterns = [
    path('', BillingListCreateView.as_view(), name='billing-list-create'),  # Notice the empty path
    path('<int:pk>/', BillingDetailView.as_view(), name='billing-detail'),
]
