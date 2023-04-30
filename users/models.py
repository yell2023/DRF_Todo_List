from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager): 
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None): # 근데 내가 슈퍼유저 만드는거에는 네임을 안넣었는데 왜 슈퍼 유저 만들때도 유저 만들 때 넣은 것들이 나오는 거지?
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser): # 필수필드 id, email, password, name, gender, age, introduction
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    username = models.CharField(max_length=255,null=False) # 공백이면 안된다라고 넣고 싶어...REQUIRED_FIELDS = []여기에는 안넣고 또 저 위에 create에 안넣었지만 내가 null=False 이렇게 해둬서 회원가입 때 이름까지 입력해야하나봄!
    gender_choices = (
        ('-', 'Select Gender'),
        ('M','Man'),
        ('W','woman')
    )
    gender = models.CharField(max_length=1, choices=gender_choices, blank=True, default='')
    age = models.IntegerField(null=True)
    # age는 생년월일을 받아서 내가 계산하는 걸로 할까?
    introduction = models.TextField(blank=True, default='')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin