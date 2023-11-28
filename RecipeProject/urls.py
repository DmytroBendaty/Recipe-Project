
from django.contrib import admin
from django.urls import path, include
from regapp import views as reg_views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('recipesapp.urls')),
    path('register/', reg_views.register, name="register"),
    path('login/', auth_views.LoginView.as_view(template_name="regapp/login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name="regapp/logout.html"), name="logout"),
    path('profile/', reg_views.profile, name="profile"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
