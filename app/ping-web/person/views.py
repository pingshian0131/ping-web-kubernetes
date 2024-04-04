import requests
import logging

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.http import JsonResponse
from django.template.loader import render_to_string

from .models import (
    Blog,
    Portfolio,
    PortfolioCategory,
    Contact,
    About,
    PersonalInformation,
    Skill,
    Introduce,
    Summary,
    Education,
    ProfessionalExperience,
    Article,
    EmailContactRecord,
    EmailRecipient,
)

logger = logging.getLogger(__name__)


def home(request):
    about = About.objects.filter(is_active=True).first()
    introduce = Introduce.objects.first()
    personal_information = PersonalInformation.objects.filter(is_active=True).order_by(
        "sort"
    )
    top_level_skills = Skill.objects.filter(parent=None).order_by("sort")
    summary = Summary.objects.first()
    education = Education.objects.all()
    professional_experience = ProfessionalExperience.objects.all()
    portfolio_category = PortfolioCategory.objects.all().order_by("priority")
    portfolio = Portfolio.objects.filter(is_active=True)
    article = Article.objects.order_by("-update_dt")[:6]
    return render(
        request,
        "home.html",
        {
            "about": about,
            "personal_information": personal_information,
            "skills": top_level_skills,
            "introduce": introduce,
            "summary": summary,
            "education": education,
            "professional_experience": professional_experience,
            "portfolio_category": portfolio_category,
            "portfolio": portfolio,
            "article": article,
            "site_key": settings.RECAPTCHA_PUBLIC_KEY,
            "action": settings.RECAPTCHA_ACTION,
        },
    )


def write_contact_record(
    name: str, email: str, subject: str, message: str, log: str, is_success: bool
):
    """儲存收信紀錄

    Args:
        name (str): 寄信人名稱
        email (str): 寄信人email
        subject (str): 主旨
        message (str): 訊息
        log (str): log
        is_success (bool): 是否成功
    """
    contact_record = EmailContactRecord(
        name=name,
        email=email,
        subject=subject,
        message=message,
        log=log,
        is_success=is_success,
    )
    contact_record.save()


def get_email_recipient() -> list:
    return EmailRecipient.objects.filter(is_active=True).values_list("email", flat=True)


def send_email(request):
    if request.method == "POST":
        data = {"result": False}

        name = request.POST.get("name", None)
        email = request.POST.get("email", None)
        subject = request.POST.get("subject", None)
        message = request.POST.get("message", None)
        if not name or not subject or not message or not email:
            return JsonResponse(data)

        g_recaptcha_response = request.POST.get("g-recaptcha-response")

        r = requests.post(
            "https://www.google.com/recaptcha/api/siteverify",
            data={
                "secret": settings.RECAPTCHA_PRIVATE_KEY,
                "response": g_recaptcha_response,
                "action": settings.RECAPTCHA_ACTION,
            },
            timeout=2,
        )
        res = r.json()
        logger.info(f"res: {res}")
        try:
            if res["success"] is True:
                if (
                    not res["score"] > 0.3
                    or not res["action"] == settings.RECAPTCHA_ACTION
                ):
                    raise PermissionDenied("reCaptcha res not passed.")
            else:
                raise PermissionDenied(res["error-codes"])

        except Exception as e:
            data["msg"] = str(e)
            logger.error(str(e))
            return JsonResponse(data)

        try:
            html_message = render_to_string(
                "email.html", {"name": name, "email": email, "message": message}
            )
            # 寄送郵件
            send_mail(
                subject=subject,
                message=message,
                from_email=f"Personal Website <{email}>",
                recipient_list=get_email_recipient(),
                fail_silently=False,
                html_message=html_message,
            )
            log = "success"
            is_success = True
            data["result"] = True
        except Exception as e:
            log = repr(e)
            is_success = False
            data["result"] = False

        write_contact_record(name, email, subject, message, log, is_success)
        return JsonResponse(data)
