from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('login/', views.log_in, name='login'),
    path('register/', views.register, name='register'),
    path('register_pi/<str:username>/', views.register_pi, name='register_pi'),
    path('logout/', views.log_out, name='logout'),
    path('forgot_pass/', views.forgot_pass, name='forgot_pass'),
    path('reset_pass/', views.reset_pass, name='reset_pass'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('create_auction/', views.create_auction, name='create_auction'),
    path('auction_details/<int:auction_id>/', views.auction_details, name='auction_details'),
    path('place_bid/<int:auction_id>/', views.place_bid, name='place_bid'),
    path('update_auction_status/', views.update_auction_status, name='update_auction_status'),
    path('watchlist/', views.watchlist, name='watchlist'),
    path('add_to_watchlist/<int:auction_id>/', views.add_to_watchlist, name='add_to_watchlist'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)