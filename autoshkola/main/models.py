from django.db import models


class SiteSettings(models.Model):
    """Настройки сайта"""
    phone = models.CharField('Телефон', max_length=100, default='8 917-236-95-35')
    address = models.CharField('Адрес', max_length=300, default='г.Альметьевск, ул. Мира 10')
    office_room = models.CharField('Кабинет записи', max_length=50, default='№312')
    work_hours = models.CharField('Время работы', max_length=200,
                                  default='понедельник-пятница с 8:00 до 16:00 (обед с 12:00 до 13:00)')
    director_name = models.CharField('Руководитель', max_length=200, default='Алаев Владимир Петрович')
    director_office = models.CharField('Кабинет руководителя', max_length=50, default='220 кабинет')
    gosposhlina_link = models.URLField('Ссылка для оплаты госпошлины', max_length=500, blank=True)

    class Meta:
        verbose_name = 'Настройки сайта'
        verbose_name_plural = 'Настройки сайта'

    def __str__(self):
        return 'Настройки сайта'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class EnrollmentPeriod(models.Model):
    """Период набора"""
    SEASON_CHOICES = [
        ('winter', 'Зимний'),
        ('spring', 'Весенний'),
        ('summer', 'Летний'),
        ('autumn', 'Осенний'),
    ]
    STATUS_CHOICES = [
        ('recording', 'Идёт запись'),
        ('completed', 'Набор завершен'),
        ('training', 'Идёт обучение'),
    ]

    season = models.CharField('Сезон', max_length=20, choices=SEASON_CHOICES)
    year = models.IntegerField('Год')
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='recording')
    recording_start = models.DateField('Начало записи', null=True, blank=True)
    recording_end = models.DateField('Конец записи', null=True, blank=True)
    training_start = models.DateField('Начало обучения', null=True, blank=True)
    med_commission_start = models.DateField('Медкомиссия с', null=True, blank=True)
    med_commission_end = models.DateField('Медкомиссия по', null=True, blank=True)
    additional_info = models.TextField('Дополнительная информация', blank=True)
    order = models.IntegerField('Порядок отображения', default=0)

    class Meta:
        verbose_name = 'Период набора'
        verbose_name_plural = 'Периоды набора'
        ordering = ['-order', '-year']

    def __str__(self):
        return f'{self.get_season_display()} период {self.year}'


class EnrollmentGroup(models.Model):
    """Группа набора"""
    period = models.ForeignKey(EnrollmentPeriod, on_delete=models.CASCADE, related_name='groups',
                               verbose_name='Период')
    group_number = models.IntegerField('Номер группы')
    max_students = models.IntegerField('Максимум студентов', default=28)
    free_places = models.IntegerField('Свободных мест', default=28)

    class Meta:
        verbose_name = 'Группа набора'
        verbose_name_plural = 'Группы набора'
        ordering = ['group_number']

    def __str__(self):
        return f'Группа №{self.group_number} ({self.period})'


class PricingInfo(models.Model):
    """Стоимость обучения"""
    student_price = models.IntegerField('Цена для студентов', default=64000)
    external_price = models.IntegerField('Цена для сторонних', default=67000)
    student_initial_payment = models.IntegerField('Первоначальный взнос студенты', default=10000)
    external_initial_payment = models.IntegerField('Первоначальный взнос сторонние', default=15000)
    training_duration = models.CharField('Срок обучения', max_length=100, default='3 месяца')
    category = models.CharField('Категория', max_length=10, default='В')

    class Meta:
        verbose_name = 'Стоимость обучения'
        verbose_name_plural = 'Стоимость обучения'

    def __str__(self):
        return f'Стоимость категория {self.category}'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class GalleryCategory(models.Model):
    """Категория галереи"""
    name = models.CharField('Название', max_length=200)
    order = models.IntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Категория галереи'
        verbose_name_plural = 'Категории галереи'
        ordering = ['order']

    def __str__(self):
        return self.name


class GalleryImage(models.Model):
    """Изображение галереи"""
    category = models.ForeignKey(GalleryCategory, on_delete=models.CASCADE, related_name='images',
                                  verbose_name='Категория')
    image = models.ImageField('Изображение', upload_to='gallery/')
    caption = models.CharField('Подпись', max_length=300, blank=True)
    order = models.IntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
        ordering = ['order']

    def __str__(self):
        return self.caption or f'Изображение {self.pk}'


class TheoreticalSchedule(models.Model):
    """Расписание теоретических занятий"""
    info_text = models.TextField('Текст расписания',
                                 default='Теоретические занятия проводятся 2 раза в неделю (понедельник-четверг) с 18:15 до 19:30, лекционные классы - 003, 023, компьютерные классы - 231, 233.')
    schedule_file = models.FileField('Файл расписания (PDF/изображение)', upload_to='schedules/', blank=True,
                                     null=True)
    schedule_image = models.ImageField('Изображение расписания', upload_to='schedules/', blank=True, null=True)

    class Meta:
        verbose_name = 'Расписание теории'
        verbose_name_plural = 'Расписание теории'

    def __str__(self):
        return 'Расписание теоретических занятий'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class DrivingSchedule(models.Model):
    """Графики вождения"""
    car_name = models.CharField('Название автомобиля', max_length=200)
    reg_number = models.CharField('Гос.номер', max_length=50)
    schedule_file = models.FileField('Файл графика', upload_to='driving_schedules/')
    start_date = models.DateField('Дата начала действия', null=True, blank=True)
    order = models.IntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'График вождения'
        verbose_name_plural = 'Графики вождения'
        ordering = ['order']

    def __str__(self):
        return f'{self.car_name} {self.reg_number}'


class ConsentInfo(models.Model):
    """Информация об оформлении согласия"""
    content = models.TextField('Содержание страницы')
    consent_file = models.FileField('Бланк заявления на согласие', upload_to='consent/', blank=True, null=True)

    class Meta:
        verbose_name = 'Оформление согласия'
        verbose_name_plural = 'Оформление согласия'

    def __str__(self):
        return 'Оформление согласия'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class Regulation(models.Model):
    """Положения"""
    title = models.CharField('Название', max_length=300)
    file = models.FileField('Файл', upload_to='regulations/')
    order = models.IntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Положение'
        verbose_name_plural = 'Положения'
        ordering = ['order']

    def __str__(self):
        return self.title


class NormativeDocument(models.Model):
    """Нормативные документы"""
    title = models.CharField('Название', max_length=500)
    file = models.FileField('Файл', upload_to='normative_docs/', blank=True, null=True)
    external_link = models.URLField('Внешняя ссылка', blank=True)
    note = models.CharField('Примечание', max_length=300, blank=True)
    order = models.IntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Нормативный документ'
        verbose_name_plural = 'Нормативные документы'
        ordering = ['order']

    def __str__(self):
        return self.title


class ExamDate(models.Model):
    """Даты выпускного экзамена"""
    group_number = models.CharField('Номер группы', max_length=50)
    exam_date = models.DateField('Дата экзамена')
    exam_time = models.TimeField('Время экзамена')
    classroom = models.CharField('Кабинет', max_length=50)
    order = models.IntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Дата выпускного экзамена'
        verbose_name_plural = 'Даты выпускного экзамена'
        ordering = ['order', 'exam_date']

    def __str__(self):
        return f'Группа №{self.group_number} - {self.exam_date}'


class GibddExamDate(models.Model):
    """Даты сдачи экзамена в РЭО ГИБДД"""
    group_number = models.CharField('Номер группы', max_length=50)
    exam_date = models.DateField('Дата экзамена')
    exam_time = models.TimeField('Время экзамена')
    additional_info = models.CharField('Дополнительная информация', max_length=300, blank=True)
    order = models.IntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Дата экзамена ГИБДД'
        verbose_name_plural = 'Даты экзамена ГИБДД'
        ordering = ['order', 'exam_date']

    def __str__(self):
        return f'Группа №{self.group_number} - {self.exam_date}'


class DocumentsPageContent(models.Model):
    """Контент страницы документов"""
    content = models.TextField('Содержание страницы (HTML)')

    class Meta:
        verbose_name = 'Страница документов'
        verbose_name_plural = 'Страница документов'

    def __str__(self):
        return 'Необходимые документы для обучения'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class FeeInfoPageContent(models.Model):
    """Контент страницы госпошлины"""
    content = models.TextField('Содержание страницы (HTML)')

    class Meta:
        verbose_name = 'Страница госпошлины'
        verbose_name_plural = 'Страница госпошлины'

    def __str__(self):
        return 'Информация о госпошлине'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class TaxReturnInfo(models.Model):
    """Информация о возврате 13%"""
    content = models.TextField('Содержание страницы (HTML)')

    class Meta:
        verbose_name = 'Возврат 13%'
        verbose_name_plural = 'Возврат 13%'

    def __str__(self):
        return 'Информация о возврате 13%'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class DrivingScheduleHeader(models.Model):
    """Заголовок графиков вождения"""
    title = models.CharField('Заголовок', max_length=300,
                             default='ГРАФИКИ ВОЖДЕНИЯ КАТ В с 15.12.2025')

    class Meta:
        verbose_name = 'Заголовок графиков вождения'
        verbose_name_plural = 'Заголовок графиков вождения'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj