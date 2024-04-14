from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from . import views
from . import user_login
urlpatterns = [
    path('admin/', admin.site.urls),
    path('base',views.base,name='base'),
    
    path('',views.home,name='home'),
    path('courses/',views.single_course,name='single_course'),
    path('product/filter-data',views.filter_data,name="filter-data"),
    path('search',views.search_course,name="search_course"),
    path('course/<slug:slug>',views.course_detail,name='course_detail'),
    path('404',views.page_not_found,name='404'),
    
    
    path('contact',views.contact_us,name='contact_us'),
    path('about_us/',views.about_us,name='about_us'),
    
    path('accounts/register',user_login.register,name='register'),
    path('accounts/',include('django.contrib.auth.urls')),
    path('doLogin',user_login.doLogin,name='doLogin'),
    path('accounts/profile',user_login.profile,name='profile'),
    path('accounts/profile/update',user_login.profile_update,name='profile_update'),
    
    path('my_course',views.my_course,name='my_course'),
    
    path('checkout/<slug:slug>',views.checkout,name='checkout'),
    
    
    
    
    
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

