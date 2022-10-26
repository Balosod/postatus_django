from django.conf import settings
from django.urls import path, re_path, include, reverse_lazy
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from .users.views import (RedirectSocial,ActivateUserEmail,GoodServicesView,
                           DashboardView, InterestView,UserProfileView,PostDeliveryView,
                           GetDeliveryView)

router = DefaultRouter()

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(router.urls)),
    path("api-token-auth/", views.obtain_auth_token),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("auth/", include("djoser.urls")),
    path("api/auth/social/", include("djoser.social.urls")),
    path("auth/", include("djoser.urls.jwt")),
    path("auth/users/activate/account/", ActivateUserEmail.as_view()),
    path('accounts/profile/', RedirectSocial.as_view()),
    #path('',include("users.url")),
    path('goods', GoodServicesView.as_view(),name= "goods"),
    path('all_goods', DashboardView.as_view(),name= "dashboard"),
    path('interest', InterestView.as_view(),name= "interest"),
    path('post_delivery', PostDeliveryView.as_view(),name= "post_delivery"),
    path('get_delivery', GetDeliveryView.as_view(),name= "get_delivery"),
    path('user', UserProfileView.as_view(),name= "user"),
    # the 'api-root' from django rest-frameworks default router
    # http://www.django-rest-framework.org/api-guide/routers/#defaultrouter
    re_path(r"^$", RedirectView.as_view(url=reverse_lazy("api-root"), permanent=False)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
