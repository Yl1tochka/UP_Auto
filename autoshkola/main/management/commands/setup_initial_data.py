from django.core.management.base import BaseCommand
from main.models import (
    SiteSettings, PricingInfo, EnrollmentPeriod, EnrollmentGroup,
    TheoreticalSchedule, DrivingScheduleHeader, ConsentInfo,
    DocumentsPageContent, FeeInfoPageContent, TaxReturnInfo,
    GalleryCategory, ExamDate, GibddExamDate, Regulation, NormativeDocument
)
from datetime import date, time


class Command(BaseCommand):
    help = 'Заполняет базу данных начальными данными'

    def handle(self, *args, **options):
        # Настройки сайта
        settings = SiteSettings.load()
        settings.phone = '8 917-236-95-35'
        settings.address = 'г.Альметьевск, ул. Мира 10'
        settings.office_room = '№312'
        settings.work_hours = 'понедельник-пятница с 8:00 до 16:00 (обед с 12:00 до 13:00)'
        settings.director_name = 'Алаев Владимир Петрович'
        settings.director_office = '220 кабинет'
        settings.save()
        self.stdout.write(self.style.SUCCESS('✅ Настройки сайта'))

        # Стоимость
        pricing = PricingInfo.load()
        pricing.student_price = 64000
        pricing.external_price = 67000
        pricing.student_initial_payment = 10000
        pricing.external_initial_payment = 15000
        pricing.training_duration = '3 месяца'
        pricing.category = 'В'
        pricing.save()
        self.stdout.write(self.style.SUCCESS('✅ Стоимость обучения'))

        # Зимний период 2026
        period1, _ = EnrollmentPeriod.objects.get_or_create(
            season='winter', year=2026,
            defaults={
                'status': 'training',
                'order': 1,
            }
        )
        for i in range(1, 4):
            EnrollmentGroup.objects.get_or_create(
                period=period1, group_number=i,
                defaults={'max_students': 28, 'free_places': 0}
            )

        # Весенний период 2026
        period2, _ = EnrollmentPeriod.objects.get_or_create(
            season='spring', year=2026,
            defaults={
                'status': 'completed',
                'training_start': date(2026, 3, 30),
                'order': 2,
            }
        )
        for i in range(1, 4):
            EnrollmentGroup.objects.get_or_create(
                period=period2, group_number=i,
                defaults={'max_students': 28, 'free_places': 0}
            )

        # Осенний период 2026
        period3, _ = EnrollmentPeriod.objects.get_or_create(
            season='autumn', year=2026,
            defaults={
                'status': 'recording',
                'recording_start': date(2026, 3, 2),
                'recording_end': date(2026, 7, 2),
                'training_start': date(2026, 9, 1),
                'med_commission_start': date(2026, 6, 1),
                'med_commission_end': date(2026, 6, 30),
                'order': 3,
            }
        )
        groups_data = [(1, 0), (2, 25), (3, 28)]
        for num, places in groups_data:
            EnrollmentGroup.objects.get_or_create(
                period=period3, group_number=num,
                defaults={'max_students': 28, 'free_places': places}
            )
        self.stdout.write(self.style.SUCCESS('✅ Периоды набора'))

        # Расписание теории
        schedule = TheoreticalSchedule.load()
        schedule.info_text = 'Теоретические занятия проводятся 2 раза в неделю (понедельник-четверг) с 18:15 до 19:30, лекционные классы - 003, 023, компьютерные классы - 231, 233.'
        schedule.save()
        self.stdout.write(self.style.SUCCESS('✅ Расписание теории'))

        # Заголовок графиков вождения
        header = DrivingScheduleHeader.load()
        header.title = 'ГРАФИКИ ВОЖДЕНИЯ КАТ В с 15.12.2025'
        header.save()
        self.stdout.write(self.style.SUCCESS('✅ Заголовок графиков'))

        # Графики вождения (без файлов, файлы загрузить через админку)
        cars = [
            ('ЛАДА Гранта', 'В 423 ОМ'),
            ('ЛАДА Гранта', 'В 008 НХ'),
            ('ЛАДА Гранта', 'М 537 МО'),
            ('ЛАДА Гранта', 'М 591 НА'),
            ('Лада Гранта', 'В 257 НХ'),
            ('ЛАДА Гранта', 'Р 165 РВ'),
            ('ЛАДА Веста', 'В 321 ОМ'),
        ]
        from main.models import DrivingSchedule
        for i, (name, reg) in enumerate(cars):
            DrivingSchedule.objects.get_or_create(
                car_name=name, reg_number=reg,
                defaults={'order': i}
            )
        self.stdout.write(self.style.SUCCESS('✅ Графики вождения'))

        # Согласие
        consent = ConsentInfo.load()
        consent.content = ''
        consent.save()
        self.stdout.write(self.style.SUCCESS('✅ Оформление согласия'))

        # Контент страниц
        DocumentsPageContent.load()
        FeeInfoPageContent.load()
        tax = TaxReturnInfo.load()
        tax.content = ''
        tax.save()
        self.stdout.write(self.style.SUCCESS('✅ Контент страниц'))

        # Категории галереи
        gallery_cats = [
            'Здание Альметьевского Политехнического техникума',
            'Класс по изучению законодательства в сфере дорожного движения',
            'Класс первой медицинской помощи при ДТП',
            'Компьютерный класс',
            'Класс по устройству и техническому обслуживанию автомобилей',
            'Классы по техническому обслуживанию автомобилей',
            'Учебный автодром',
            'Учебные автомобили',
        ]
        for i, name in enumerate(gallery_cats):
            GalleryCategory.objects.get_or_create(name=name, defaults={'order': i})
        self.stdout.write(self.style.SUCCESS('✅ Категории галереи'))

        # Даты выпускного экзамена
        exam_dates_data = [
            ('143', date(2026, 3, 25), time(18, 15), '231 кабинет'),
            ('144', date(2026, 3, 26), time(18, 15), '233 кабинет'),
            ('145', date(2026, 3, 27), time(18, 15), '231 кабинет'),
        ]
        for i, (group, d, t, room) in enumerate(exam_dates_data):
            ExamDate.objects.get_or_create(
                group_number=group, exam_date=d,
                defaults={'exam_time': t, 'classroom': room, 'order': i}
            )
        self.stdout.write(self.style.SUCCESS('✅ Даты выпускного экзамена'))

        # Даты ГИБДД
        gibdd_dates_data = [
            ('143', date(2026, 3, 31), time(10, 0)),
            ('144', date(2026, 4, 2), time(8, 0)),
            ('145', date(2026, 4, 3), time(8, 0)),
        ]
        for i, (group, d, t) in enumerate(gibdd_dates_data):
            GibddExamDate.objects.get_or_create(
                group_number=group, exam_date=d,
                defaults={'exam_time': t, 'order': i}
            )
        self.stdout.write(self.style.SUCCESS('✅ Даты ГИБДД'))

        # Положения (без файлов)
        regs = [
            'Положение о допуске к выпускному экзамену',
            'Положение о сдаче выпускного экзамена',
            'Положение о сдаче экзамена в РЭО ГИБДД',
            'Положение о пересдаче экзамена в РЭО ГИБДД',
            'Положение о получении водительского удостоверения',
        ]
        for i, title in enumerate(regs):
            Regulation.objects.get_or_create(title=title, defaults={'order': i})
        self.stdout.write(self.style.SUCCESS('✅ Положения'))

        # Нормативные документы
        norm_docs = [
            'Заключение ГИБДД по РТ о соответствии учебно-материальной базы установленным требованиям (категория «B»)',
            'Заключение ГИБДД по РТ о соответствии учебно-материальной базы установленным требованиям (категория «C»)',
            'Программа подготовки водителей',
            'Лицензия на осуществление образовательной деятельности',
            'Приложение к лицензии',
            'Образец договора на оказание платных образовательных услуг на курсах подготовки водителей',
            'Устав ГАПОУ «Альметьевский политехнический техникум»',
            'Правила внутреннего трудового распорядка в ГАПОУ «Альметьевский политехнический техникум»',
            'Постановление Правительства РФ от 15 сентября 2020 г. №1441',
            'Положение об оказании платных образовательных услуг в ГАПОУ «Альметьевский политехнический техникум»',
            'Единый государственный реестр юридических лиц',
            'Положение о дополнительном профессиональном образовании в ГАПОУ «Альметьевский политехнический техникум»',
        ]
        for i, title in enumerate(norm_docs):
            note = ''
            if 'дополнительном профессиональном' in title:
                note = 'Нет такого файла'
            NormativeDocument.objects.get_or_create(title=title, defaults={'order': i, 'note': note})
        self.stdout.write(self.style.SUCCESS('✅ Нормативные документы'))

        self.stdout.write(self.style.SUCCESS('\n🎉 Все начальные данные успешно загружены!'))
        self.stdout.write(self.style.WARNING('\n⚠️  Не забудьте:'))
        self.stdout.write('   1. Загрузить файлы положений через админку')
        self.stdout.write('   2. Загрузить файлы нормативных документов через админку')
        self.stdout.write('   3. Загрузить файлы графиков вождения через админку')
        self.stdout.write('   4. Загрузить фотографии в галерею через админку')
        self.stdout.write('   5. Загрузить бланк заявления на согласие через админку')