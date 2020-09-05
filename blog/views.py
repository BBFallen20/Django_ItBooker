from django.shortcuts import get_object_or_404
from django.views import generic
from django.views.generic.edit import FormMixin
from .models import Book, Author, Genre
from django.db.models import Q, F
from adlist.models import Ad
from .forms import CommentForm
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .custom.csmm import CustomSuccessMessageMixin
from django.contrib.auth.forms import UserCreationForm


class UserProfileView(generic.DetailView):
    model = User
    template_name = 'registration/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_ads'] = Ad.objects.filter(author_id=self.request.user.id)
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(User, id=self.kwargs['user'])


class RegisterFormView(generic.edit.FormView):
    """Страница формы регистрации пользователя"""
    form_class = UserCreationForm

    success_url = '/'

    template_name = 'registration/register.html'

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)

    def form_invalid(self, form):
        return super(RegisterFormView, self).form_invalid(form)


class BookList(generic.ListView):
    """Страница списка книг"""
    template_name = 'blog/book_list.html'
    model = Book
    paginate_by = 5

    def get_queryset(self):
        """Может принимать жанр, по которому будут выданы все подходящие книги, либо отображать все существующие"""
        category = self.kwargs.get('name', None)
        if category is not None:
            return Book.objects.filter(genre__name=category)
        else:
            return Book.objects.all()

    def get_context_data(self, **kwargs):
        """Доп. информация для страницы: название жанра, если таков имеется, список всех жанров"""
        context = super().get_context_data(**kwargs)
        context['name'] = self.kwargs.get('name', None)
        context['genres'] = Genre.objects.all()
        return context


class AuthorDetail(generic.DetailView):
    """Подробная страница об авторе"""
    model = Author
    template_name = 'blog/author-detail.html'

    def get_context_data(self, **kwargs):
        """Доп. информация: все книги данного автора"""
        context = super().get_context_data(**kwargs)
        context['author_books'] = Book.objects.filter(author_id=self.kwargs.get('pk', None))
        return context


class BookDetail(CustomSuccessMessageMixin, FormMixin, generic.DetailView):
    """Подробная информация о книге"""
    model = Book
    template_name = 'blog/book-detail.html'
    form_class = CommentForm
    success_msg = 'Комментарий успешно создан.'

    def get_success_url(self, **kwargs):
        return reverse_lazy('blog:book-detail', kwargs={'slug': self.get_object().slug})

    def get_object(self, queryset=None):
        Book.objects.filter(slug__iexact=self.kwargs['slug']).update(count=F('count') + 1)
        return get_object_or_404(Book, slug__iexact=self.kwargs['slug'])

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.book = self.get_object()
        self.object.save()
        return super().form_valid(form)


class SearchView(generic.ListView):
    """Страница поиска"""
    model = Book
    template_name = 'blog/search.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Book.objects.filter(
            Q(title__icontains=query) | Q(author__first_name__icontains=query) | Q(author__last_name__icontains=query)
        )


class MainView(generic.TemplateView):
    template_name = 'blog/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Book.objects.all()[:3]
        context['ads'] = Ad.objects.all()[:3]
        return context

