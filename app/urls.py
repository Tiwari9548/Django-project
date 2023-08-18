from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from . forms import LoginForm , MyPasswordResetForm , MyPasswordChangeForm , MySetPasswordForm

urlpatterns = [
    path('',views.home,name='home'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),

    path('category/<slug:val>',views.CategoryView,name='category'),
    path('category/<val>',views.CategoryTitle,name='category-title'),
    path('productdetail/<int:pk>',views.ProductDetail,name='productdetail'),
    path('profile/',views.ProfileView.as_view(),name='profile'),
    path('address/',views.address,name='address'),
    path('updateAddress/<int:pk>',views.UpdateAddress.as_view(),name='UpdateAddress'),
    path('address/',views.address,name='address'),

    
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/',views.show_cart, name='showcart'),
    path('checkout/',views.checkout.as_view(), name='checkout'),

    path('search/',views.search, name='search'),

    path('pluscart/',views.plus_cart, name='pluscart'),
    path('minuscart/',views.minus_cart, name='minuscart'),
    path('removecart/',views.remove_cart, name='removecart'),

    








    
    



    #login authentication

    path('registration/',views.CustomerRegistrationView.as_view(),name='customerregistration'),
    path('accounts/login/',auth_view.LoginView.as_view(template_name='app/login.html', authentication_form=LoginForm),name='login'),
    
    path('passwordchange/',auth_view.PasswordChangeView.as_view(template_name='app/changepassword.html', form_class=MyPasswordChangeForm, success_url='/passwordchangedone'), name='passwordchange'),
    path('passwordchangedone/',auth_view.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'), name='passwordchangedone'),
    path('logout/',auth_view.LogoutView.as_view(next_page='login'), name='logout'),
     
    path('password-reset/',auth_view.PasswordResetView.as_view(template_name='app/password_reset.html', form_class=MyPasswordResetForm),name='password_reset'),  
    path('password-reset/done/',auth_view.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uiddb64>/<token>' , auth_view.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html'), name='password_reset_complete'),  
    path('password-reset-complete/',auth_view.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'),name='password_reset_complete'),
    
    



]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)