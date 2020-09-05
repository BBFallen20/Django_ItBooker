from django.views import generic
from django.shortcuts import get_object_or_404
from .models import Ad, Category
from django.urls import reverse_lazy
from django.db.models import Q, F
from blog.custom.csmm import CustomSuccessMessageMixin
from django.views.generic.edit import FormMixin
from .forms import CommentForm


class AdListView(generic.ListView):
    """Отображение списка статей"""
    model = Ad
    template_name = 'adlist/ad_list.html'
    paginate_by = 5  # Пагинация после 5 статей на странице

    def get_queryset(self):
        """Функция вывода статей из БД на сайт.
        В функцию может быть передана категория статей по которой осуществляется фильтрация вывода.
        Если категория не передается - выводится полный список статей."""
        category = self.kwargs.get('name', None)
        if category is not None:
            return Ad.objects.filter(category__name=category)
        else:
            return Ad.objects.all()

    def get_context_data(self, **kwargs):
        """Доп. данные для вывода на страницу: название категории, если такова имеется,
         список всех категорий."""
        context = super().get_context_data(**kwargs)
        context['name'] = self.kwargs.get('name', None)
        context['genres'] = Category.objects.all()
        return context


class AdDetailView(FormMixin, CustomSuccessMessageMixin, generic.DetailView):
    """Подробная информация о статье"""
    model = Ad
    template_name = 'adlist/ad_detail.html'
    success_msg = 'Комментарий успешно создан.'
    form_class = CommentForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('adlist:ad-detail', kwargs={'slug': self.get_object().slug})

    def get_object(self, queryset=None):
        Ad.objects.filter(slug__iexact=self.kwargs['slug']).update(count=F('count') + 1)
        return get_object_or_404(Ad, slug__iexact=self.kwargs['slug'])

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.ad = self.get_object()
        self.object.save()
        return super().form_valid(form)


class SearchView(generic.ListView):
    """Поиск по статьям"""
    model = Ad
    template_name = 'adlist/search.html'

    def get_queryset(self):
        """Запрос из поисковой строки передается в фильтр по объектам базы данных
         и при совпадении выводится на странице"""
        query = self.request.GET.get('q')
        return Ad.objects.filter(
            # Поиск по названию статьи и названию источника статьи
            Q(title__icontains=query) | Q(source__title__icontains=query)
        )
