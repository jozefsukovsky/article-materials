from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render


def demo_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('demo_view')
    else:
        form = AuthenticationForm() if not request.user.is_authenticated else None
    
    if request.user.is_authenticated:
        # Initialize or increment the session counter
        request.session['visit_count'] = request.session.get('visit_count', 0) + 1
        session_count = request.session['visit_count']
    else:
        session_count = None
    
    context = {
        'form': form,
        'session_count': session_count
    }
    return render(request, 'account/demo.html', context)


def logout_view(request):
    logout(request)
    return redirect('demo_view')
