from django.shortcuts import render
from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404
from .forms import PostForm, CommentForm
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.db.models import Q
from django.views.generic import ListView, DetailView, CreateView
from django.http import HttpResponse



class PostsListView(ListView): # представление в виде списка
    model = Post                   # модель для представления 

class PostDetailView(DetailView): # детализированное представление модели
    model = Post

from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm

class RegisterFormView(FormView):
    form_class = UserCreationForm


    # Ссылка, на которую будет перенаправляться пользователь в случае успешной регистрации.
    # В данном случае указана ссылка на страницу входа для зарегистрированных пользователей.
    success_url = "/login/"

    # Шаблон, который будет использоваться при отображении представления.
    template_name = "register.html"

    def form_valid(self, form):
        # Создаём пользователя, если данные в форму были введены корректно.
        form.save()

        # Вызываем метод базового класса
        return super(RegisterFormView, self).form_valid(form)

# Опять же, спасибо django за готовую форму аутентификации.
from django.contrib.auth.forms import AuthenticationForm

# Функция для установки сессионного ключа.
# По нему django будет определять, выполнил ли вход пользователь.
from django.contrib.auth import login

class LoginFormView(FormView):
    form_class = AuthenticationForm

    # Аналогично регистрации, только используем шаблон аутентификации.
    template_name = "login.html"

    # В случае успеха перенаправим на главную.
    success_url = "/postlist"

    def form_valid(self, form):
        # Получаем объект пользователя на основе введённых в форму данных.
        self.user = form.get_user()

        # Выполняем аутентификацию пользователя.
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)

from django.http import HttpResponseRedirect
from django.views.generic.base import View
from django.contrib.auth import logout

class LogoutView(View):
    def get(self, request):
        # Выполняем выход для пользователя, запросившего данное представление.
        logout(request)

        # После чего, перенаправляем пользователя на главную страницу.
        return HttpResponseRedirect("/login")

def post_list(request):
	if request.user.is_authenticated:
		posts = Post.objects.all()
		return render(request,'blog/post_list.html',{'posts':posts})
	else:
	    return render(request, 'unauth.html')


def post_detail(request, pk):
	if request.user.is_authenticated:
	    post = get_object_or_404(Post, pk=pk)
	    comments = post.comments.filter(active=True)


	    if request.method == 'POST':
	        comment_form = CommentForm(data=request.POST)
	        if comment_form.is_valid():
	            new_comment = comment_form.save(commit=False)
	            new_comment.post = post
	            new_comment.name = request.user
	            new_comment.save()

	    else:
	        comment_form = CommentForm()
	    return render(request,
	                  'blog/post_detail.html',
	                 {'post': post,
	                  'comments': comments,
	                  'comment_form': comment_form,})
	else:
	    return render(request, 'unauth.html')


def post_new(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                return redirect('post_detail', pk=post.pk)
        else:
            form = PostForm()
        return render(request, 'blog/post_edit.html', {'form': form})
    else:
        return render(request, 'unauth.html')


def post_edit(request, pk):
	if request.user.is_authenticated:
		post = get_object_or_404(Post, pk=pk)
		if request.user == post.author:
			if request.method == "POST":
				form = PostForm(request.POST, instance=post)
				if form.is_valid():
					post = form.save(commit=False)
					post.author = request.user
					post.save()
				return redirect('post_detail', pk=post.pk)
			else:
				form = PostForm(instance=post)
			return render(request, 'blog/post_change.html', {'form': form})
		else:
			return render(request, 'not_owner.html')
	else:
	    return render(request, 'unauth.html')

def user_post(request, username):
	if request.user.is_authenticated:
		posts = Post.objects.filter(author=username)
		return render(request,'blog/post_list.html',{'posts':posts})
	else:
	    return render(request, 'unauth.html')

def users(request):
	if request.user.is_authenticated:
		if request.user.is_superuser:
			posts=Post.objects.all()
			users = []
			us_id = []
			for post in posts:
				users.append((str(post.author), int(post.author.id)))
				#us_id.append(int(post.author.id))
			spis_user = list(set(users))
			#spis_id = list(set(us_id))

				#users.append[(str(post.author), int(post.author.id))]
			#users = list(set(users))
			#posts1 = Post.objects.all()
			return render(request,'users.html', {'users': spis_user})
		else:
			message = 'Вы не являетесь суперпользователем'
			return HttpResponse(message)
	else:
	    return render(request, 'unauth.html')

checking = {}
def add_like(request, pk):
	#print(checking)
	if request.user.is_authenticated:
		post = get_object_or_404(Post, pk=pk)
		#try:
			#checking[str(pk)]+=str(post.author.id)+' '
		#except KeyError:
			#checking[str(pk)]=str(post.author.id)+' '
		#spis = checking[str(pk)].split()
		#print(spis)
		#spis1 = [int(i) for i in spis]
		#if all(int(post.author.id)for i in spis1):
			#return render(request, 'cannot_like.html')

		if pk in request.COOKIES:

			return render(request, 'cannot_like.html')
		else:
			post.likes += 1
			post.save()
			response = redirect('post_detail', pk=post.pk)
			response.set_cookie(pk, int(post.author.id))
			return response
	else:
	    return render(request, 'unauth.html')
	#return redirect('post_detail', pk=post.pk)
def post_delete(request, pk):
	if request.user.is_authenticated:

		post = get_object_or_404(Post, pk=pk)
		if request.user == post.author:
			post.delete()
			return HttpResponseRedirect("/postlist")
		else:
			return render(request, 'not_owner.html')
	else:
	    return render(request, 'unauth.html')



def search_user(request):
	if request.user.is_authenticated:

		return render(request,'search.html')

	else:
	    return render(request, 'unauth.html')


def search_text(request):
	if request.user.is_authenticated:

		return render(request,'searchtext.html')

	else:
	    return render(request, 'unauth.html')

def search(request):
	if request.user.is_authenticated:
		q = request.GET['q']
		if q:
			i = 0
			posts = Post.objects.all()
			login = request.GET.get('q')
			#print(login)
			for post in posts:
				if str(post.author)==str(login):
					us_id = int(post.author.id)
					i+=1
					break
			if i==0:	
				message = 'Вы искали пользователя: %r ,которого не существует' % request.GET['q']
				return HttpResponse(message)


			posts = Post.objects.filter(author=us_id)
			#for post in posts:
			#	print(post)
			#	if q==posts.author:
			#us_id = posts.author.id
			#posts1 = Post.objects.filter(author=us_id[0])
			return render(request,'blog/post_list.html',{'posts':posts})
			#else:
			#return render(request, 'search_error.html')
	    #if 'q' in request.GET:
	        #message = 'You searched for: %r' % request.GET['q']
	        #return HttpResponse(message)
		else:
			message = 'You submitted an empty form.'
			return HttpResponse(message)

	else:
		return render(request, 'unauth.html')



def searchtext(request):
	if request.user.is_authenticated:
		q = request.GET['q']
		if q:
			i = 0
			posts = Post.objects.all()
			text = request.GET.get('q')



				
			posts = Post.objects.filter(Q(title__icontains=text))
			#for post in posts:
				#if str(post)!='Post object':
					#message = 'Вы искали следующее: %r . К сожалнию нет совпадений' % request.GET['q']
					#return HttpResponse(message)

			return render(request,'blog/post_list.html',{'posts':posts})
		else:
			message = 'You submitted an empty form.'
			return HttpResponse(message)

	else:
		return render(request, 'unauth.html')

def sort_likes(request): 
	posts = Post.objects.all().order_by('likes') 
	return render(request,'blog/post_list.html',{'posts':posts})		
