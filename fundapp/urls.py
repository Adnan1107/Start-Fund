from django.urls import path
from .import views

urlpatterns=[
    path('',views.home,name='home'),
    
    path('register/',views.register,name='register'),
    path('profile/',views.profile,name='profile'),
    path('login/',views.login,name='login'),
    path('userhome/',views.userhome,name='userhome'),
    path('edit/<int:eid>/',views.edit,name='edit'),
    path('delete/',views.delete,name='delete'),
    path('admin_dashboard/',views.admin_dashboard,name='admin_dashboard'),
    path('admin_userlist/',views.admin_userlist,name='admin_userlist'),
    path('founderregistration/',views.founderregistration,name='founderregistration'),
    path('investerregistration/',views.investerregistration,name='investerregistration'),
    path('founderlist/',views.founderlist,name='founderlist'),

    path('invest/',views.invest,name='invest'),

    path('edit/<int:eid>/', views.edit, name='edit_profile'),

    path('founderindex/',views.founderindex, name='founderindex'),
    path('founderlogin/',views.founderlogin,name='founderlogin'),
    path('logout/',views.logout,name='logout'),
    # path('investorindex/',views.investorindex, name='investorindex'),
    path('investorlogin/', views.investorlogin, name='investorlogin'),
    path('inprofile/',views.investorprofile,name='inprofile'),
    path('investoredit/<int:eid>/',views.investoredit,name='investoredit'),
    path('investordeleteconfirm/',views.investordeleteconfirm,name='investordeleteconfirm'),
    path('indelete/',views.indelete,name='indelete'),
    path('submit_contact/', views.submit_contact, name='submit_contact'),
    path('profile/', views.profile, name='profile'),
    path('investor_home/', views.investor_home, name='investor_home'),
    path('founder_home/', views.founder_home, name='founder_home'),
    path('founder_pro/',views.founder_profile,name='founder_pro'),

    path('investlist/',views.investlist,name='investlist'),
    path('investorslist/',views.investorslist,name='investorslist'),
    path('deleteinvest/<int:iid>/',views.deleteinvest,name='deleteinvest'),


    path('investors/',views.investors,name='investors'),

    path('amt/',views.amt,name='amt'),



    path('view_startups/', views.view_startups, name='view_startups'),
    path('addstartup/', views.add_startup, name='addstartup'),

    path('view_startups_user/', views.view_startups_user, name='view_startups_user'),
    path('startupedit/<int:eid>/', views.startupedit, name='startupedit'),
    path('startupdelete/<int:eid>/', views.startupdelete, name='startupdelete'),


    path('payment/<int:startupid>/', views.handle_payment, name='handle_payment'),
    path('payment/verify/', views.verify_payment, name='verify_payment'),    
    path('chat/',views.chat_list,name='chat_list'),
    path('chat/<str:user_type>/<str:username>/', views.chat_detail, name='chat_detail'),
    path('about/', views.about, name='about'),
    path('fodelete/', views.fodelete, name='fodelete'),
    path('investnamedetails/',views.investnamedetails,name='investnamedetails'),
    path('sell_investment/<int:investment_id>/', views.sell_investment, name='sell_investment'),
]


