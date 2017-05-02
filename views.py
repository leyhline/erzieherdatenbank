from django.views.generic import ListView, DetailView, View

from .models import Activity, FieldOfEducation, Material, Season, Tag, Festival


class ActivityList(ListView):
    model = Activity


class ActivityDetail(DetailView):
    model = Activity


class FieldOfEducationList(ListView):
    model = FieldOfEducation


class FieldOfEducationDetail(DetailView):
    model = FieldOfEducation


class MaterialList(ListView):
    model = Material


class MaterialDetail(DetailView):
    model = Material


class SeasonList(ListView):
    model = Season


class SeasonDetail(DetailView):
    model = Season


class TagList(ListView):
    model = Tag


class TagDetail(DetailView):
    model = Tag

class FestivalList(ListView):
    model = Festival

class FestivalDetail(DetailView):
    model = Festival