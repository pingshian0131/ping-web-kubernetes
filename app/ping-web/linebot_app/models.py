from django.db import models


class LineBotUser(models.Model):
    class AccountStatus(models.TextChoices):
        DEFAULT = "0", "預設"
        R = "1", "註冊中"

    display_name = models.CharField(
        "使用者名稱",
        max_length=20,
        default="",
        blank=True,
    )

    line_user_id = models.CharField(
        "使用者LineUserID",
        max_length=33,
        default="",
        blank=True,
        unique=True,
    )

    status = models.CharField(
        "狀態",
        max_length=1,
        choices=AccountStatus.choices,
        default=AccountStatus.DEFAULT,
    )

    bind_status = models.BooleanField(
        "已綁定",
        default=False,
    )
    pub_date = models.DateTimeField("創建日期", auto_now_add=True)
    last_updated_date = models.DateTimeField("最後更新日期", auto_now=True)

    class Meta:
        verbose_name = "Line帳號管理"
        verbose_name_plural = "Line帳號管理"

    def __str__(self):
        return self.display_name
