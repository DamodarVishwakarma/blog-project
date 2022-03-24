from django.urls import path
from core.views import ProfileView, ActivateAccount, SignUpView

urlpatterns = [

    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/<int:pk>/', ProfileView.as_view(template_name='commons/profile.html'), name='profile'),

    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
    # path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
    #      ActivateAccount.as_view(), name='activate'),
    # path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #      ActivateAccount.as_view(), name='activate'),
]
