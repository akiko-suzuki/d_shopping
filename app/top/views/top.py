from django.shortcuts import render, redirect


def top(request):
    print('きてる')
    return render(request, 'top/top.html', {})
