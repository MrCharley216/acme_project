from django.views.generic import TemplateView
from birthday.models import Birthday


class HomePage(TemplateView):
    """Выводим главную страницу."""

    template_name = 'pages/index.html'

    def get_context_data(self, **kwargs):
        """Добавляем контекст для счётчика записей о днях рождения."""
        context = super().get_context_data(**kwargs)
        context['total_count'] = Birthday.objects.count()
        return context
