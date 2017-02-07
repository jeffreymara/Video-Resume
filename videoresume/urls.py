from django.conf.urls import url
from videoresume import views

urlpatterns = [
    url(r'^$', views.edit_profile),
    url(r'^ajax/$', views.ajax),
    url(r'^sign-up/$', views.sign_up),
    url(r'^create-posting/$', views.create_posting),
    url(r'^profile/$', views.profile),
    url(r'^companies/$', views.companies),
    url(r'^candidates/$', views.candidates),
    url(r'^terms-and-conditions/$', views.terms_and_conditions),
    url(r'^privacy-policy/$', views.privacy_policy),
    url(r'^edit-profile/(?P<edit_profile_page>[-\w]+)/$', views.edit_profile),
]