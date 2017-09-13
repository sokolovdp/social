# GROUPS VIEWS.PY
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import generic
from django.shortcuts import get_object_or_404
from groups.models import Group, GroupMember
from django.contrib import messages

from . import models


# Create your views here.

class CreateGroup(LoginRequiredMixin, generic.CreateView):
    fields = ('name', 'description')
    model = Group


class SingleGroup(generic.DetailView):
    model = Group


class ListGroups(generic.ListView):
    model = Group


class JoinGroup(LoginRequiredMixin, generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:single', kwargs={'slug': self.kwargs.get('slug')})

    def get(self, request, *args, **kwargs):
        group = get_object_or_404(Group, slug=self.kwargs.get('slug'))
        try:
            GroupMember.objects.create(user=self.request.user, group=group)
        except:
            messages.warning(self.request, 'Warning already a member')
        else:
            messages.success(self.request, 'You are a member now!')

        return super().get(request, *args, **kwargs)


class LeaveGroup(LoginRequiredMixin, generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse("groups:single", kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):
        try:
            membership = models.GroupMember.objects.filter(
                user=self.request.user,
                group__slug=self.kwargs.get("slug")
            ).get()
        except:
            messages.warning(self.request, "You can't leave this group because you aren't in it.")
        else:
            membership.delete()
            messages.success(self.request, "You have successfully left this group.")
        return super().get(request, *args, **kwargs)
