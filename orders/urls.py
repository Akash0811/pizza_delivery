from django.urls import path

from orders import views

urlpatterns = [
    path("<int:order_id>/index", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("loginmenu", views.loginmenu, name="loginmenu"),
    path("register", views.register, name="register"),
    path("logout", views.logout_view, name="logout"),
    path("<int:order_id>/menu", views.menu, name="menu"),
    path("<int:order_id>/<int:dish_id>/<int:type_id>/rest", views.rest, name="rest"),
    path("<int:order_id>/<int:dish_id>/sub", views.sub, name="sub"),
    path("<int:order_id>/<int:dish_id>/regular_pizza", views.regular_pizza, name="regular_pizza"),
    path("<int:order_id>/<int:dish_id>/sicilian_pizza", views.sicilian_pizza, name="sicilian_pizza"),
    path("<int:order_id>/view", views.view, name="view"),
    path("", views.welcome, name="welcome"),
    path("confirmed_orders", views.confirmed_orders, name="confirmed_orders"),
    path("<int:order_id>/<int:item_id>/<int:type_id>/remove", views.remove, name="remove"),
]
