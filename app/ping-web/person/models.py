from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from mdeditor.fields import MDTextField


class Blog(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_published = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=50)
    tags = models.CharField(max_length=100)
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class PortfolioCategory(models.Model):
    category = models.CharField(max_length=255, verbose_name="類別")
    priority = models.PositiveIntegerField(default=0, verbose_name="優先順序")

    def save(self, *args, **kwargs):
        if not self.priority:
            # 如果 priority 未設置，則自動遞增
            max_priority = (
                PortfolioCategory.objects.aggregate(models.Max("priority"))[
                    "priority__max"
                ]
                or 0
            )
            self.priority = max_priority + 1
        super(PortfolioCategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.category


class Portfolio(models.Model):
    images = models.ImageField(upload_to="portfolio/")
    alt_text = models.CharField(max_length=50)
    title = models.CharField(max_length=50, verbose_name="標題")
    description = models.CharField(max_length=50, verbose_name="描述")
    url = models.URLField(max_length=100, verbose_name="網址")
    category = models.ForeignKey(
        PortfolioCategory, on_delete=models.CASCADE, verbose_name="類別"
    )
    is_active = models.BooleanField(default=True, verbose_name="啟用")

    def __str__(self):
        return self.title


class Article(models.Model):
    title = models.CharField(max_length=100, verbose_name="Article標題")
    images = models.ImageField(upload_to="portfolio/")
    url = models.URLField(max_length=200)
    content = models.TextField(verbose_name="Article內容")
    create_dt = models.DateTimeField(auto_now_add=True, verbose_name="建立時間")
    update_dt = models.DateTimeField(auto_now=True, verbose_name="更新時間")


class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name


class Introduce(models.Model):
    about_introduce = models.TextField(verbose_name="About簡介", default="", blank=True)
    about_introduce_job = models.TextField(verbose_name="About職業簡介", default="", blank=True)
    about_introduce_bottom = models.TextField(verbose_name="Aboute最下方簡介", default="", blank=True)
    skills_introduce = models.TextField(verbose_name="Skills簡介", default="", blank=True)
    resume_introduce = models.TextField(verbose_name="Resume簡介", default="", blank=True)
    portfolio_introduce = models.TextField(verbose_name="Portfolio簡介", default="", blank=True)
    articles_introduce = models.TextField(verbose_name="Articles簡介", default="", blank=True)


class About(models.Model):
    img = models.ImageField("大頭照", upload_to="about/")
    job_title = models.CharField(max_length=100, verbose_name="職稱")
    is_active = models.BooleanField(default=False, verbose_name="啟用")


class PersonalInformation(models.Model):
    info = models.CharField(max_length=50, unique=True, verbose_name="個資名稱")
    value = models.CharField(max_length=50, verbose_name="個資值")
    sort = models.PositiveIntegerField(default=0, verbose_name="顯示順序")
    is_active = models.BooleanField(default=True, verbose_name="啟用")

    def save(self, *args, **kwargs):
        if not self.sort:
            # 如果 sort 未設置，則自動遞增
            max_sort = (
                PersonalInformation.objects.aggregate(models.Max("sort"))["sort__max"]
                or 0
            )
            self.sort = max_sort + 1
        super(PersonalInformation, self).save(*args, **kwargs)


class Skill(MPTTModel):
    skill_name = models.CharField(max_length=100, unique=True, verbose_name="技能名稱")
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )
    sort = models.PositiveIntegerField(default=0, verbose_name="顯示順序")

    def save(self, *args, **kwargs):
        if not self.sort and not self.parent:
            # 只有當沒有父節點且 sort 未設置時，才自動遞增
            max_sort = (
                Skill.objects.filter(parent__isnull=True).aggregate(models.Max("sort"))[
                    "sort__max"
                ]
                or 0
            )
            self.sort = max_sort + 1
        super(Skill, self).save(*args, **kwargs)

    class MPTTMeta:
        order_insertion_by = ["skill_name"]

    def __str__(self):
        return self.skill_name


class Summary(models.Model):
    content = MDTextField()


class Education(models.Model):
    title = models.CharField(max_length=50, verbose_name="Education title")
    content = MDTextField()


class ProfessionalExperience(models.Model):
    title = models.CharField(
        max_length=50, verbose_name="Professional Experience title"
    )
    content = MDTextField()


class EmailContactRecord(models.Model):
    name = models.CharField(max_length=100, verbose_name="寄件人")
    email = models.EmailField(verbose_name="寄件人email")
    subject = models.CharField(max_length=200, verbose_name="訊息主旨")
    message = models.TextField(verbose_name="訊息內容")
    log = models.TextField(verbose_name="收信log")
    is_success = models.BooleanField(verbose_name="發送是否成功")
    date_received = models.DateTimeField(auto_now_add=True, verbose_name="接收時間")

    def __str__(self):
        return f"Message from {self.name}"


class EmailRecipient(models.Model):
    email = models.EmailField(verbose_name="收件人email")
    is_active = models.BooleanField(verbose_name="啟用")
