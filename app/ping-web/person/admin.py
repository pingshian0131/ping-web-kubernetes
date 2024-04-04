from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Portfolio,
    About,
    PersonalInformation,
    Skill,
    Introduce,
    Summary,
    Education,
    ProfessionalExperience,
    PortfolioCategory,
    Article,
    EmailContactRecord,
    EmailRecipient,
)
from mptt.admin import MPTTModelAdmin


@admin.register(PortfolioCategory)
class PortfolioCategoryAdmin(admin.ModelAdmin):
    list_display = ("category", "priority")
    list_filter = ("category", "priority")


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ("title", "images", "alt_text", "url", "category")
    list_filter = ("title", "category")


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    readonly_fields = ("create_dt", "update_dt")
    list_display = (
        "title",
        "img_preview",
        "url",
        "content_preview",
        "create_dt",
        "update_dt",
    )
    list_filter = ("title", "create_dt", "update_dt")

    @admin.display(description="內容預覽")
    def content_preview(self, obj):
        return obj.content[:100] if obj.content else ""

    @admin.display(description="圖片預覽")
    def img_preview(self, obj):
        return format_html(f"<img href='{obj.images}'>") if obj.images else ""


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ("job_title", "is_active")


@admin.register(PersonalInformation)
class PersonalInformationAdmin(admin.ModelAdmin):
    list_display = ("info", "value", "sort", "is_active")


@admin.register(Skill)
class SkillAdmin(SortableAdminMixin, MPTTModelAdmin):
    list_display = ("skill_name",)
    search_fields = ("skill_name",)
    ordering = ["sort"]


@admin.register(Introduce)
class IntroducesAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Introduce._meta.get_fields()]
    search_fields = [field.name for field in Introduce._meta.get_fields()]


@admin.register(Summary)
class SummaryAdmin(admin.ModelAdmin):
    list_display = ("content",)
    search_fields = ("content",)


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ("title",)
    search_fields = ("title",)


@admin.register(ProfessionalExperience)
class ProfessionalExperienceAdmin(admin.ModelAdmin):
    list_display = ("title",)
    search_fields = ("title",)


@admin.register(EmailContactRecord)
class EmailContactRecordAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "subject",
        "message",
        "log",
        "is_success",
        "date_received",
    )
    search_fields = (
        "name",
        "email",
        "subject",
        "message",
        "log",
        "is_success",
        "custom_date_received",
    )


@admin.register(EmailRecipient)
class EmailRecipientAdmin(admin.ModelAdmin):
    list_display = ("email", "is_active")
    search_fields = ("email", "is_active")
