from django.conf import settings
from django.urls import path, re_path, include, reverse_lazy
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from .users.views import (RedirectSocial,ActivateUserEmail,UserProfile)
from .services.views import GoodServices
from .interest.views import Interest
from .explore.views import Explore
from .detail.views import ExploreDetail
from .dashboard.views import Dashboard

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
    path('services', GoodServices.as_view(),name= "services"),
    path('explore', Explore.as_view(),name= "explore"),
    path('dashboard', Dashboard.as_view(),name= "dashboard"),
    path('explore_detail', ExploreDetail.as_view(),name= "explore_detail"),
    path('interest', Interest.as_view(),name= "interest"),
    path('user', UserProfile.as_view(),name= "user"),
    # the 'api-root' from django rest-frameworks default router
    # http://www.django-rest-framework.org/api-guide/routers/#defaultrouter
    re_path(r"^$", RedirectView.as_view(url=reverse_lazy("api-root"), permanent=False)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
