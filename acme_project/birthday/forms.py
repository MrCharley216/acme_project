from django import forms
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from .models import Birthday
from .validators import real_age

BEATLES = {'Джон Леннон', 'Пол Маккартни', 'Джордж Харрисон', 'Ринго Старр'}


class BirthdayForm(forms.ModelForm):
    """Форма для создания записи о днях рождения."""

    class Meta():
        """Метаданные формы."""

        model = Birthday
        exclude = ('author',)
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'})
        }
        validators = (real_age,)

    def clean_first_name(self):
        """Вывод одного имени(первого)."""
        # Получаем значение имени из словаря очищенных данных.
        first_name = self.cleaned_data['first_name']
        # Разбиваем полученную строку по пробелам
        # и возвращаем только первое имя.
        return first_name.split()[0]

    def clean(self):
        super().clean()
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        if f'{first_name} {last_name}' in BEATLES:
            # Отправляем письмо, если кто-то представляется
            # именем одного из участников Beatles.
            send_mail(
                subject='Another Beatles member',
                message=f'{first_name} {last_name} пытался опубликовать запись!',
                from_email='birthday_form@acme.not',
                recipient_list=['admin@acme.not'],
                fail_silently=True,
            )
            raise ValidationError(
                'Мы тоже любим Битлз, но введите, пожалуйста, настоящее имя!'
            )

# Второй метод валидатора для проверки даты рождения.
# from django import forms
# # Импортируем класс ошибки валидации.
# from django.core.exceptions import ValidationError

# from .models import Birthday

# # Множество с именами участников Ливерпульской четвёрки.
# BEATLES = {'Джон Леннон', 'Пол Маккартни', 'Джордж Харрисон', 'Ринго Старр'}


# class BirthdayForm(forms.ModelForm):

#     class Meta:
#         ...

#     def clean_first_name(self):
#         ...

#     def clean(self):
#         # Получаем имя и фамилию из очищенных полей формы.
#         super().clean()
#         first_name = self.cleaned_data['first_name']
#         last_name = self.cleaned_data['last_name']
#         # Проверяем вхождение сочетания имени и фамилии во множество имён.
#         if f'{first_name} {last_name}' in BEATLES:
#             raise ValidationError(
#                 'Мы тоже любим Битлз, но введите, пожалуйста, настоящее имя!'
#             )
