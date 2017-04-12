from django.conf.urls import url

from . import views


app_name = 'activities'
urlpatterns = [
    url(r'^(angebot/)?$', views.ActivityList.as_view(), name="activity-list"),
    url(r'^angebot/(?P<pk>[0-9]+)/$', views.ActivityDetail.as_view(), name='activity-detail'),
    url(r'^bildungsbereich/$', views.FieldOfEducationList.as_view(), name="foe-list"),
    url(r'^bildungsbereich/(?P<pk>[0-9]+)/$', views.FieldOfEducationDetail.as_view(), name="foe-detail"),
    url(r'^material/$', views.MaterialList.as_view(), name="material-list"),
    url(r'^material/(?P<pk>[0-9]+)/$', views.MaterialDetail.as_view(), name="material-detail"),
    url(r'^jahreszeit/$', views.SeasonList.as_view(), name="season-list"),
    url(r'^jahreszeit/(?P<pk>[FSHW])/$', views.SeasonDetail.as_view(), name="season-detail"),
    url(r'^tag/$', views.TagList.as_view(), name="tag-list"),
    url(r'^tag/(?P<pk>[0-9]+)/$', views.TagDetail.as_view(), name="tag-detail"),
]
