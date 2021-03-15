from django.shortcuts import render, redirect
from django.views.generic import (
    UpdateView,
    )
# from .models import Account
# from .forms import AccountForm
#UserCreationFormを使うと楽らしいので導入。
from django.contrib.auth.forms import UserCreationForm
#ログインしていないと、create/update/deleteできない様にする
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


def signup(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('art-home')  #後でlogin機能を作ったら、ここも(‘login’)に変える方が良いらしい。
	else:
		form = UserCreationForm()
	return render(request, 'account/signup.html', {'form': form}) #これは後でまた作成する

# class AccountUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
#     model = Account #これを加えるだけ。
#     template_name = 'account/account_form.html'
#     form_class = AccountForm

#     def upload(self, request):
#         form = AccountForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#         else:
#             return render(request, self.template_name, {'form':form},)
    
#     #今ログインしているユーザーが著者であることを指すためのコード。
#     def form_valid(self,form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)

#     def test_func(self): 
#         post = self.get_object()
#         if self.request.user == post.author:
#             return True
#         return False