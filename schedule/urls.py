from django.conf.urls import url
from rest_framework import routers

from schedule import views

router = routers.DefaultRouter()
router.register(r'event', views.EventViewSet)
router.register(r'course', views.PurchaseCourseViewSet)
router.register(r'rule', views.RuleViewSet)
router.register(r'calendar', views.CalendarViewSet)

urlpatterns = [
    url(r'^event/analytics/$', views.EventAnalyticsView.as_view(),
        name="event_analytics"),
]

urlpatterns += router.urls
