
from django.urls import path
from. import views

urlpatterns = [
    path("", views.index, name="shopHome"),
    path("about/", views.about, name="AboutUs"),
    path("contact/", views.contact, name="ContactUs"),
    path("tracker/", views.tracker, name="TrackingStatus"),
    path("search/", views.search, name="search"),
    path("productview/<int:myid>", views.productview, name="Productview"),
    path("checkout/", views.checkout, name="Checkout"),
    path("handlerequest/", views.handlerequest, name="handlerequest"),

]