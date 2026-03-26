from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('enrollment/', views.enrollment, name='enrollment'),
    path('documents/', views.documents, name='documents'),
    path('fee-info/', views.fee_info, name='fee_info'),
    path('gallery/', views.gallery, name='gallery'),
    path('schedule/', views.schedule, name='schedule'),
    path('driving-schedules/', views.driving_schedules, name='driving_schedules'),
    path('tax-return/', views.tax_return, name='tax_return'),
    path('consent/', views.consent, name='consent'),
    path('regulations/', views.regulations, name='regulations'),
    path('normative-docs/', views.normative_docs, name='normative_docs'),
    path('exam-dates/', views.exam_dates, name='exam_dates'),
    path('gibdd-dates/', views.gibdd_dates, name='gibdd_dates'),
]