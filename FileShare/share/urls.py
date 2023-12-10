from django.urls import path
from . import views

urlpatterns = [
    path("addfile", views.addfile, name="addfile"),
    path("home",views.home,name="home"),
    path("file_view/<path:file_name>",views.pdf_view,name="file_view"),
    path("delete_file/<int:file_id>",views.delete_file,name="delete_file"),
    path("signin",views.signin,name="signin"),
    path("signup",views.signup,name="signup"),
    path("signout",views.signout,name="signout"),
    path("peers",views.view_users,name="view_users"),
    path("peers/<int:user_id>",views.user_profile,name="user_profile"),
    path("import/<int:file_id>",views.import_file,name="import_file"),
    path("files",views.all_files,name="all_files")
]