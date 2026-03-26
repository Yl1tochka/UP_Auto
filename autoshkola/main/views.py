from django.shortcuts import render
from .models import (
    SiteSettings, EnrollmentPeriod, PricingInfo,
    GalleryCategory, TheoreticalSchedule, DrivingSchedule,
    ConsentInfo, Regulation, NormativeDocument, ExamDate, GibddExamDate,
    DocumentsPageContent, FeeInfoPageContent, TaxReturnInfo, DrivingScheduleHeader
)


def index(request):
    settings = SiteSettings.load()
    context = {
        'settings': settings,
    }
    return render(request, 'main/index.html', context)


def enrollment(request):
    pricing = PricingInfo.load()
    periods = EnrollmentPeriod.objects.prefetch_related('groups').all()
    context = {
        'pricing': pricing,
        'periods': periods,
    }
    return render(request, 'main/enrollment.html', context)


def documents(request):
    content = DocumentsPageContent.load()
    context = {
        'content': content,
    }
    return render(request, 'main/documents.html', context)


def fee_info(request):
    content = FeeInfoPageContent.load()
    settings = SiteSettings.load()
    context = {
        'content': content,
        'settings': settings,
    }
    return render(request, 'main/fee_info.html', context)


def gallery(request):
    categories = GalleryCategory.objects.prefetch_related('images').all()
    context = {
        'categories': categories,
    }
    return render(request, 'main/gallery.html', context)


def schedule(request):
    schedule_info = TheoreticalSchedule.load()
    context = {
        'schedule_info': schedule_info,
    }
    return render(request, 'main/schedule.html', context)


def driving_schedules(request):
    header = DrivingScheduleHeader.load()
    schedules = DrivingSchedule.objects.all()
    context = {
        'header': header,
        'schedules': schedules,
    }
    return render(request, 'main/driving_schedules.html', context)


def tax_return(request):
    info = TaxReturnInfo.load()
    context = {
        'info': info,
    }
    return render(request, 'main/tax_return.html', context)


def consent(request):
    info = ConsentInfo.load()
    context = {
        'info': info,
    }
    return render(request, 'main/consent.html', context)


def regulations(request):
    regs = Regulation.objects.all()
    context = {
        'regulations': regs,
    }
    return render(request, 'main/regulations.html', context)


def normative_docs(request):
    docs = NormativeDocument.objects.all()
    context = {
        'documents': docs,
    }
    return render(request, 'main/normative_docs.html', context)


def exam_dates(request):
    dates = ExamDate.objects.all()
    context = {
        'dates': dates,
    }
    return render(request, 'main/exam_dates.html', context)


def gibdd_dates(request):
    dates = GibddExamDate.objects.all()
    context = {
        'dates': dates,
    }
    return render(request, 'main/gibdd_dates.html', context)