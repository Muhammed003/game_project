from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView, ListView

from apps.account.forms import UserForm
from apps.account.mixins import RoleRequiredMixin
from apps.account.models import CustomUser


class SignInView(View):
    template_name = 'account/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        phone_number = f"+{request.POST.get('phone_number')}"
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')

        user = authenticate(request=request, phone_number=phone_number, password=password)
        if user is not None:
            login(request, user)
            if remember_me == "on":

                request.session.set_expiry(60 * 60 * 24 * 30)  # 30 days if "remember me" is checked
            else:
                request.session.set_expiry(60 * 60 * 24 * 7)
            return redirect('/')
        else:
            error_message = "Invalid phone number or password"
            return render(request, self.template_name, {'error_message': error_message})





class UserListView(RoleRequiredMixin, TemplateView):
    template_name = 'account/control_users.html'

    def get(self, request):
        user = self.request.user
        users = []
        if user.roles == "admin":
            users = CustomUser.objects.all().order_by("username")
        else:
            users = CustomUser.objects.filter(country=user.country).order_by("username")

        return render(request, self.template_name, {"users": users})

from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserForm
from .models import CustomUser
from .mixins import RoleRequiredMixin


class UserCreateView(RoleRequiredMixin, TemplateView):
    template_name = "account/users_form.html"

    def get(self, request):
        form = UserForm(request=request)  # передаем request
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = UserForm(request.POST, request=request)  # передаем request
        if form.is_valid():
            form.save()
            return redirect("user-list")
        return render(request, self.template_name, {"form": form})


class UserUpdateView(RoleRequiredMixin, TemplateView):
    template_name = "account/users_form.html"

    def get(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        form = UserForm(instance=user, request=request)  # передаем request
        return render(request, self.template_name, {"form": form, "edit": True})

    def post(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        form = UserForm(request.POST, instance=user, request=request)  # передаем request
        if form.is_valid():
            form.save()
            return redirect("user-list")
        return render(request, self.template_name, {"form": form, "edit": True})


class UserDeleteView(RoleRequiredMixin, TemplateView):
    def get(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        user.delete()
        return redirect("user-list")


class NoPermissionPageView(TemplateView):
    template_name = "account/no-permission-page.html"