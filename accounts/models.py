from django.contrib.auth.models import AbstractUser, AbstractBaseUser


class User(AbstractUser):
    pass

# this is just to try things out
class NewUser(AbstractBaseUser):
    pass

