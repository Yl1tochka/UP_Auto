from django.contrib import admin
from .models import (
    SiteSettings, EnrollmentPeriod, EnrollmentGroup, PricingInfo,
    GalleryCategory, GalleryImage, TheoreticalSchedule, DrivingSchedule,
    ConsentInfo, Regulation, NormativeDocument, ExamDate, GibddExamDate,
    DocumentsPageContent, FeeInfoPageContent, TaxReturnInfo, DrivingScheduleHeader
)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'phone', 'address')

    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False


class EnrollmentGroupInline(admin.TabularInline):
    model = EnrollmentGroup
    extra = 1


@admin.register(EnrollmentPeriod)
class EnrollmentPeriodAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'status', 'training_start', 'order')
    list_editable = ('status', 'order')
    inlines = [EnrollmentGroupInline]


@admin.register(PricingInfo)
class PricingInfoAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'student_price', 'external_price')

    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False


class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    extra = 1


@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    list_editable = ('order',)
    inlines = [GalleryImageInline]


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'category', 'order')
    list_filter = ('category',)
    list_editable = ('order',)


@admin.register(TheoreticalSchedule)
class TheoreticalScheduleAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(DrivingSchedule)
class DrivingScheduleAdmin(admin.ModelAdmin):
    list_display = ('car_name', 'reg_number', 'start_date', 'order')
    list_editable = ('order',)


@admin.register(DrivingScheduleHeader)
class DrivingScheduleHeaderAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ConsentInfo)
class ConsentInfoAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Regulation)
class RegulationAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)


@admin.register(NormativeDocument)
class NormativeDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'note')
    list_editable = ('order',)


@admin.register(ExamDate)
class ExamDateAdmin(admin.ModelAdmin):
    list_display = ('group_number', 'exam_date', 'exam_time', 'classroom', 'order')
    list_editable = ('order',)


@admin.register(GibddExamDate)
class GibddExamDateAdmin(admin.ModelAdmin):
    list_display = ('group_number', 'exam_date', 'exam_time', 'order')
    list_editable = ('order',)


@admin.register(DocumentsPageContent)
class DocumentsPageContentAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(FeeInfoPageContent)
class FeeInfoPageContentAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(TaxReturnInfo)
class TaxReturnInfoAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False