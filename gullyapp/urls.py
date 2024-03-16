from django.urls import include,path
from . import views
from django.conf.urls.static import static
urlpatterns = [
    
    path('', views.home, name="home"),
    path('index/',views.index, name="index"),
    path('main/',views.main, name="main"),
    path('admin-login/',views.adminLogin, name="admin_login"),
    path('adminhome/',views.adminHome, name="adminhome"),
    path('admindashboard/',views.admin_dashboard, name="admindashboard"),
    path('add-category/',views. add_category, name="add_category"),
    path('view-category/',views. view_category, name="view-category"),
    path('edit-category/<int:pid>/', views.edit_category, name="edit_category"),
    path('delete-category/<int:pid>/', views.delete_category, name="delete_category"),
    path('create_team/', views.create_team, name='create_team'),
    path('registration/', views.registration, name="registration"),
    path('userlogin/',views.userlogin, name="userlogin"),
    path('profile/',views.profile, name="profile"),
    path('logout/', views.logoutuser, name="logout"),
    path('adminlogout/', views.adminlogout, name="adminlogout"),
    path('change-password/', views.change_password, name="change_password"),
    path('join_team/<int:pid>/', views.view_team, name="join_team"),
    path('team_detail/<int:pid>/', views.team_detail, name="team_detail"),
    #path('view_opponents/', views.view_opponents, name='view_opponents'),
    #notification
    #path('notifications/', views.view_notifications, name='view_notifications'),
    path('search_opponents/', views.search_opponents, name='search_opponents'),
    path('challenge_opponent/<str:team_captain_username>/', views.challenge_opponent, name='challenge_opponent'),
    path('accept-challenge/<str:team_captain_username>/', views.accept_opponent, name='accept_challenge'),
    path('reject-challenge/<str:team_captain_username>/', views.rejectopponent, name='reject_challenge'),
     #path('notifications/', views.notification_panel, name='notification_panel'),
     #path('fetch_nearby_teams/', views.fetch_nearby_teams, name='fetch_nearby_teams'),
    path('admin-change-password/',views.admin_change_password, name="admin_change_password"),
    path('manage-user/',views.manage_user, name="manage_user"),
    path('delete-user/<int:pid>/', views.delete_user, name="delete_user"),
    path('add_team/', views.add_team, name="add_team"),
    path('adminview_team/', views.adminview_team, name="adminview_team"),
    path('edit_teams/<int:pid>/', views.edit_teams, name="edit_teams"),
    path('delete-team/<int:pid>/', views.delete_team, name="delete_team"),
    #notificationurls
    
    
    
    path('infocard/<int:pid>/', views.infocard, name="infocard"),
    path('acceptedcard/<int:pid>/', views.acceptedcard, name="acceptedcard"),

    path('get_requested_user_details/', views.get_requested_user_details, name='get_requested_user_details'),

    #join
    
    #path('joinclan/', views.joinclan, name="joinclan"),
    path('joinclan/<int:pid>/', views.joinclan, name="joinclan"),
    path('clan/<int:clan_id>/', views.clan, name="clan"),

    #path('leave_clan/<int:pid>/', views.leave_clan, name="leave_clan"),
    path('leave_team/', views.leave_team, name='leave_team'),
    


    #path('join_clan/<int:team_id>/', views.join_clan, name='join_clan'),



     
    
    
    
    
    

   
]


from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    
    re_path(r'ws/notifications/$', consumers.NotificationConsumer.as_asgi()),
]

