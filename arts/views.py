from django.shortcuts import render, redirect, get_object_or_404
#own
from django.conf import settings
import neuralStyleProcess
from django.urls import reverse
from django.http import JsonResponse

import cv2

# Create your views here.
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    DeleteView,
    )
from .models import Arts, Like, User
from .forms import ArtsForm
#ログインしていないと、create/update/deleteできない様にする
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class ArtsListView(ListView):
    model = Arts
    template_name = "arts/home.html"
    context_object_name = 'arts'
    ordering = ['-date']

    def get_context_data(self, **kwargs):
        
        #ユーザーがいいねした記事一覧を拾うために記載
        arts = Arts.objects.all()
        liked_list = []
        for art in arts:
            #ログインしている場合
            if self.request.user.is_active:
                liked = art.like_set.filter(user=self.request.user)
            #ログインしていない場合はこうしないとエラーが出る。
            else:
                liked = art.like_set.none()

            if liked.exists():
                liked_list.append(art.id)

        context = super(ArtsListView, self).get_context_data(**kwargs)
        context.update({
            'arts': Arts.objects.all().order_by('?'),
            #（参考）Action別にフィルターをかけたい場合の方法
            'arts_udnie': Arts.objects.filter(action='UDNIE').order_by('-date'),
            # いいねした一覧
            'liked_list': liked_list,
        })
        return context


class ArtsDetailView(DetailView):
    model = Arts
    template_name = "arts/art_detail.html"
    #objectでもOK, artでも使えるようにする
    context_object_name = 'art'

    def get_context_data(self, **kwargs):
        
        #ユーザーがいいねした記事一覧を拾うために記載
        arts = Arts.objects.all()
        liked_list = []
        for art in arts:
            #ログインしている場合
            if self.request.user.is_active:
                liked = art.like_set.filter(user=self.request.user)
            #ログインしていない場合は以下としないとエラーが出る。
            else:
                liked = art.like_set.none()

            if liked.exists():
                liked_list.append(art.id)

        context = super(ArtsDetailView, self).get_context_data(**kwargs)
        context.update({
            # いいねした一覧
            'liked_list': liked_list
        })
        return context


class ArtsCreateView(LoginRequiredMixin, CreateView):
    template_name = 'arts/art_form.html'
    form_class = ArtsForm

    def upload(self, request):
        form = ArtsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        else:
            return render(request, self.template_name, {'form':form},)

    #今ログインしているユーザーが著者であることを指すためのコード。
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)  


class ArtsDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Arts
    template_name = 'arts/art_confirm_delete.html'
    form_class = ArtsForm
    success_url = '/'

    # ログインユーザーしか削除できないようにする。
    def test_func(self): 
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
        
#カテゴリー別に表示
class CategoryView(ListView):
    model = Arts
    template_name = 'arts/art_category.html'
    context_object_name = 'arts'

    def get_queryset(self):
        # action = Arts.objects.get(action=self.kwargs['action'][0])
        queryset = Arts.objects.order_by('-id').filter(action=self.kwargs['action'])
        return queryset

    #アクセスした値を取得し辞書に格納
    def get_context_data(self, **kwargs):
        
        #ユーザーがいいねした記事一覧を拾うために記載
        arts = Arts.objects.all()
        liked_list = []
        for art in arts:
            #ログインしている場合
            if self.request.user.is_active:
                liked = art.like_set.filter(user=self.request.user)
            #ログインしていない場合は以下としないとエラーが出る。
            else:
                liked = art.like_set.none()

            if liked.exists():
                liked_list.append(art.id)

        context = super().get_context_data(**kwargs)
        context.update({
            'category_key' : self.kwargs['action'],
            # いいねした一覧
            'liked_list': liked_list,
        })
        #context['category_key'] = self.kwargs['action']
        return context

#自分の投稿を表示
class MyArtView(LoginRequiredMixin, ListView):
    model = Arts
    template_name = "arts/mylist.html"
    context_object_name = 'arts'
    ordering = ['-date']

    def get_context_data(self, **kwargs):
        
        # ユーザーがいいねした記事一覧を拾うために記載
        arts = Arts.objects.all()
        liked_list = []
        for art in arts:
            #ログインしている場合
            if self.request.user.is_active:
                liked = art.like_set.filter(user=self.request.user)
            #ログインしていない場合は以下としないとエラーが出る。
            else:
                liked = art.like_set.none()

            if liked.exists():
                liked_list.append(art.id)
        context = super(MyArtView, self).get_context_data(**kwargs)
        context.update({
            'mylist': Arts.objects.filter(author=self.request.user).order_by('-date'),
            'liked_list': liked_list,
        })
        return context


#自分がいいねした投稿を表示
class MyLikeView(LoginRequiredMixin, ListView):
    model = Arts
    template_name = "arts/mylist.html"
    context_object_name = 'arts'
    ordering = ['-date']

    def get_context_data(self, **kwargs):
        arts = Arts.objects.all()
        liked_list = []
        for art in arts:
            #ログインしている場合
            if self.request.user.is_active:
                liked = art.like_set.filter(user=self.request.user)
            #ログインしていない場合は以下としないとエラーが出る。
            else:
                liked = art.like_set.none()

            if liked.exists():
                liked_list.append(art.id)

        context = super(MyLikeView, self).get_context_data(**kwargs)
        context.update({
            #fileterのかけかたが特徴的なので覚えておくこと！
            'mylist': Arts.objects.filter(like__user__in=[self.request.user]).order_by('-date'),
            'liked_list': liked_list,
        })
        return context


#いいね機能実装のため
def LikeView(request):
    if request.method =="POST":
        art = get_object_or_404(Arts, pk=request.POST.get('art_id'))
        user = request.user
        liked = False
        like = Like.objects.filter(art=art, user=user)
        if like.exists():
            like.delete()
        else:
            like.create(art=art, user=user)
            liked = True
    
        context={
            'art_id': art.id,
            'liked': liked,
            'count': art.like_set.count(),
        }

    if request.is_ajax():
        return JsonResponse(context)

#How To Useページ追加
class ArtsHowToUseView(ListView):
    model = Arts
    template_name = "arts/art_instruction.html"
    #objectでもOK, artでも使えるようにする
    context_object_name = 'art'

    def get_context_data(self, **kwargs):
        
        context = super(ArtsHowToUseView, self).get_context_data(**kwargs)
        
        return context