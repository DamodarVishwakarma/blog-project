from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, UpdateView
from core.forms import SignUpForm, ProfileForm
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.contrib.auth import login
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from core.tokens import account_activation_token
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate


class SignUpView(View):
    User = get_user_model()
    form_class = SignUpForm
    template_name = 'commons/signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, mail_subject='Welcome in my blog site', *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate account till it is confirmed
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate Your Core Account'
            message = render_to_string('emails/account_activation_email.html', {

                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')

        return render(request, self.template_name, {'form': form})


class ActivateAccount(View):
    def activate(request, uidb64, token):
        User = get_user_model()
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        else:
            return HttpResponse('Activation link is invalid!')


class ProfileView(LoginRequiredMixin, UpdateView):
    User = get_user_model()
    model = User
    form_class = ProfileForm
    success_url = reverse_lazy('home')
    template_name = 'commons/profile.html'
