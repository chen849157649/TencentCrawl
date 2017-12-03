from django.shortcuts import redirect
from django.core.urlresolvers import reverse


def check_on(view_func):
    def wrapper(request, *view_args, **view_kwargs):
        if request.session.has_key('is_login'):
            return view_func(request, *view_args, **view_kwargs)
        else:
            return redirect(reverse('user:login'))
    return wrapper
