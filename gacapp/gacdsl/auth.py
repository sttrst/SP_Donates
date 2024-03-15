from django.contrib.auth.backends import BaseBackend
from .models import DiscordUser


class DiscordAuthBackend(BaseBackend):
    def authenticate(self, request, user) -> DiscordUser:
        find_user = DiscordUser.objects.filter(id=user['id'])
        if len(find_user) == 0:
            print('USER WAS NOT FOUND. CREATING NEW')
            new_user = DiscordUser.objects.create_new_discord_user(user)
            print('CREATED A NEW USER:', new_user)
            return new_user
        return find_user

    def get_user(self, user_id):
        try:
            return DiscordUser.objects.get(pk=user_id)
        except DiscordUser.DoesNotExist:
            return None
