from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    """A form for creating users. Includes all the required."""

    class Meta(UserCreationForm.Meta):
        """Include the fields that are required in addition to the required fields."""

        model = User
        fields = ('username', 'bio')