from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
from django.urls import reverse_lazy
from .models import Birthday
from .forms import BirthdayForm
from .utils import calculate_birthday_countdown


class OnlyAuthorMixin(UserPassesTestMixin):

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user


class BirthdayMixin:
    """Миксин для вывода списка записей о днях рождения."""

    model = Birthday
    form_class = BirthdayForm


class BirthdayListView(ListView):
    """Выводим список всех записей в БД."""

    model = Birthday
    ordering = 'id'
    paginate_by = 10


class BirthdayCreateView(BirthdayMixin, CreateView):
    """Выводим форму для создания записи о днях рождения."""

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class BirthdayUpdateView(OnlyAuthorMixin, BirthdayMixin, UpdateView):
    """Выводим форму для редактирования записи о днях рождения."""

    pass


class BirthdayDeleteView(OnlyAuthorMixin, DeleteView):
    """Удаляем запись из БД."""

    model = Birthday
    success_url = reverse_lazy('birthday:list')


class BirthdayDetailView(DetailView):
    """Выводим детали записи о днях рождения."""

    model = Birthday
    template_name_suffix = '_detail'

    def get_context_data(self, **kwargs):
        """Добавляем контекст для подсчета 'осталось дней до дня рождения'."""
        context = super().get_context_data(**kwargs)
        context['birthday_countdown'] = calculate_birthday_countdown(
            self.object.birthday)
        return context
