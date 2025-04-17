from django.db import models
from django.urls import reverse


class Classes(models.Model):
    name = models.CharField(max_length=20, verbose_name='Название')
    image = models.ImageField(upload_to='photos/classes/%m/%Y/%d/', blank=True)
    sub_classes = models.ManyToManyField('SubClasses', verbose_name='Подклассы', related_name='subclasses')
    description = models.TextField(blank=True, verbose_name='Описание')
    main_chars = models.ManyToManyField('Chars', verbose_name='Основная характеристика',
                                        related_name='classes_main_chars')
    hit_dice = models.ForeignKey('Dices', on_delete=models.PROTECT, verbose_name='Кость хитов')
    first_level_hits = models.IntegerField(verbose_name='Хиты на первом уровне')
    another_levels_hits = models.IntegerField(verbose_name='Хиты на следующий уровнях')
    saving_throws = models.ManyToManyField('Chars', verbose_name='Спасброски', related_name='classes_saving_trows')
    weapons_ownership = models.ManyToManyField('WeaponsCategories', verbose_name='Владение оружием',
                                               related_name='classes_weapons', blank=True)
    weapons_ownership_add = models.CharField(max_length=100, verbose_name='Дополнение к владению оружием', blank=True)
    skills_ownership = models.ManyToManyField('Skills', verbose_name='Владение навыками', related_name='classes_skills',
                                              blank=True)
    skills_ownership_add = models.CharField(max_length=100, verbose_name='Дополнение к владению навыками', blank=True)
    tools_ownership = models.ManyToManyField('Tools', verbose_name='Владение инструментами',
                                             related_name='classes_tools', blank=True)
    tools_ownership_add = models.CharField(max_length=100, verbose_name='Дополнение к владению инструментами',
                                           blank=True)
    armors_ownership = models.ManyToManyField('ArmorCategories', verbose_name='Владение доспехами',
                                              related_name='classes_armors', blank=True)
    armors_ownership_add = models.CharField(max_length=100, verbose_name='Дополнение к владению доспехами', blank=True)
    becoming = models.TextField(verbose_name='Становление')
    beginning_equipment = models.TextField(verbose_name='Стартовое снаряжение', blank=True)
    levels = models.ManyToManyField('Levels', related_name='class_levels', verbose_name='Уровни')
    spells = models.ManyToManyField('Spells', related_name='class_spells', verbose_name='Заклинания', blank=True)
    source = models.ForeignKey('Sources', on_delete=models.PROTECT, verbose_name='Источник')

    # def get_absolute_url(self):
    #     return reverse('classes', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Класс'
        verbose_name_plural = 'Классы'


class Chars(models.Model):
    name = models.CharField(max_length=20, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Характеристика'
        verbose_name_plural = 'Характеристики'


class Dices(models.Model):
    value = models.PositiveSmallIntegerField(verbose_name='Кость', )

    def __str__(self):
        return f'd{self.value}'

    class Meta:
        verbose_name = 'Кость'
        verbose_name_plural = 'Кости'


# FIXME не очень понял, это прям отдельная модель?
#  т.е. у тебя есть просто предмет, а есть конкретные предметы, которые ничем не отключаются,
#  но лежат в разных таблицах? (Weapons, DruidicFocuses и тд?)
#  если так, то все таблицы, которые не имеют собственных уникальные аттрибутов
#  можно сложить в одну таблицу, но добавить просто ItemType.
#  Мб это и ок, но те таблицы, у которых нет собственных уникальных аттрибутов,
#  точно следовало бы сделать иначе (пример я описал выше)
class Items(models.Model):
    name = models.CharField(max_length=35, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    weight = models.FloatField(null=True, verbose_name='Вес')
    price = models.IntegerField(null=True, verbose_name='Стоимость')
    source = models.ForeignKey('Sources', on_delete=models.PROTECT, verbose_name='Источник')

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'

    def __str__(self):
        return self.name

    def price_correct_display(self) -> str:
        correct_price: int = self.price
        if correct_price / 10 >= 1:
            if correct_price / 100 >= 1:
                return f'{correct_price / 100} зм'
            else:
                return f'{correct_price / 10} см'
        else:
            return f'{correct_price} мм'


class WeaponsCategories(models.Model):
    name = models.CharField(max_length=20, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')

    def __str__(self):
        return f'{self.name} оружие'

    class Meta:
        verbose_name = 'Категория оружия'
        verbose_name_plural = 'Категории оружий'


class WeaponClasses(models.Model):
    name = models.CharField(max_length=20, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Класс оружия'
        verbose_name_plural = 'Классы оружий'


class WeaponsFeatures(models.Model):
    name = models.CharField(max_length=20, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Свойство оружия'
        verbose_name_plural = 'Свойства оружий'


class WeaponsTechniques(models.Model):
    name = models.CharField(max_length=20, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    source = models.ForeignKey('Sources', on_delete=models.PROTECT, verbose_name='Источник')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Оруженый прием'
        verbose_name_plural = 'Оружейные приемы'


class DamageTypes(models.Model):
    name = models.CharField(max_length=20, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Примеры')

    class Meta:
        verbose_name = 'Тип урона'
        verbose_name_plural = 'Типы урона'

    def __str__(self):
        return self.name


class Weapons(Items, models.Model):
    category = models.ForeignKey('WeaponsCategories', on_delete=models.PROTECT, verbose_name='Категория')
    weapon_class = models.ForeignKey('WeaponClasses', on_delete=models.PROTECT, verbose_name='Класс')
    damage_dice = models.ForeignKey('Dices', on_delete=models.PROTECT, verbose_name='Кость урона')
    damage_dices_quantity = models.IntegerField(verbose_name='Количество костей')
    damage_type = models.ForeignKey('DamageTypes', on_delete=models.PROTECT, verbose_name='Тип урона')
    features = models.ManyToManyField('WeaponsFeatures', blank=True, verbose_name='Свойства',
                                      related_name='weapons_features')
    technique = models.ForeignKey('WeaponsTechniques', on_delete=models.PROTECT, verbose_name='Оружейные приемы')

    def damage_correct_display(self) -> str:
        return f'{self.damage_dices_quantity}{self.damage_dice} {self.damage_type}'

    class Meta:
        verbose_name = 'Оружие'
        verbose_name_plural = 'Оружия'


class Sources(models.Model):
    name = models.CharField(max_length=4, verbose_name='Источник')
    description = models.TextField(blank=True, verbose_name='Описание')
    icon = models.ImageField(blank=True, verbose_name='Иконка', upload_to='photos/sources/%m/%Y/%d/')

    # FIXME это что?)
    #  как минимум, неправильная аннотация, т.к. у тебя сейчас метод возвращает str | None
    #  а скорее всего, он должен возвращать строго строку.
    def get_absolute_url(self,
                         model: str) -> str:
        if model == 'classes':
            return reverse('class_to_source', kwargs={'source_id': self.pk})

    class Meta:
        verbose_name = 'Источник'
        verbose_name_plural = 'Источники'

    def __str__(self):
        return self.name


class Skills(models.Model):
    name = models.CharField(max_length=20, verbose_name='Название')
    char = models.ForeignKey('Chars', on_delete=models.PROTECT, verbose_name='Характеристика')
    description = models.TextField(blank=True, verbose_name='Пример использования')

    class Meta:
        verbose_name = 'Навык'
        verbose_name_plural = 'Навыки'

    def __str__(self):
        return self.name


class Tools(Items, models.Model):
    char = models.ForeignKey('Chars', on_delete=models.PROTECT, verbose_name='Характеристика')
    use = models.TextField(blank=True, verbose_name='Использование')
    create = models.TextField(blank=True, verbose_name='Создание')

    class Meta:
        verbose_name = 'Инструмент'
        verbose_name_plural = 'Инструменты'


class ArmorCategories(models.Model):
    name = models.CharField(max_length=20, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Категория доспеха'
        verbose_name_plural = 'Категории доспехов'

    def __str__(self):
        return self.name


class Armors(Items, models.Model):
    category = models.ForeignKey('ArmorCategories', on_delete=models.PROTECT, verbose_name='Категория')
    # FIXME аттрибуты моделей называются всегда в lower кейсе
    #  капсом можно объявлять всякие константы
    AC = models.IntegerField(verbose_name='КД')
    AC_add = models.CharField(max_length=100, verbose_name='Дополнение к КД', null=False, blank=True)
    strength = models.IntegerField(verbose_name='Минимум силы', null=False, blank=True)
    stealth = models.BooleanField(verbose_name='Помеха скрытности', default=False)

    class Meta:
        verbose_name = 'Доспех'
        verbose_name_plural = 'Доспехи'


# FIXME вот про эти модели я писал выше, они выглядят избыточными
class ArcaneFocuses(Items, models.Model):
    class Meta:
        verbose_name = 'Магическая фокусировка'
        verbose_name_plural = 'Магические фокусировки'


class HolySymbols(Items, models.Model):
    class Meta:
        verbose_name = 'Священный символ'
        verbose_name_plural = 'Священные символы'


class DruidicFocuses(Items, models.Model):
    class Meta:
        verbose_name = 'Фокусировка друидов'
        verbose_name_plural = 'Фокусировки друидов'
# FIXME


class Levels(models.Model):
    name = models.CharField(max_length=30, verbose_name='Название уровня')
    level_number = models.IntegerField(verbose_name='Номер уровня')
    level_description = models.TextField(verbose_name='Описание уровня', blank=True)

    class Meta:
        verbose_name = 'Уровень'
        verbose_name_plural = 'Уровни'

    def __str__(self):
        return self.name


class SubClasses(models.Model):
    sub_class_name = models.CharField(max_length=40, verbose_name='Подкласс')
    sub_class_description = models.TextField(verbose_name='Описание подкласса', blank=True)
    image = models.ImageField(upload_to='photos/classes/sub_classes/%m/%Y/%d/', blank=True)
    levels = models.ManyToManyField('Levels', related_name='subclass_levels')
    source = models.ForeignKey('Sources', on_delete=models.PROTECT, verbose_name='Источник')
    spells = models.ManyToManyField('Spells', related_name='sub_class_spells', verbose_name='Заклинания', blank=True)

    class Meta:
        verbose_name = 'Подкласс'
        verbose_name_plural = 'Подклассы'

    def __str__(self):
        return self.sub_class_name


class Spells(models.Model):
    name = models.CharField(max_length=40, verbose_name='Название')
    level = models.IntegerField(verbose_name='Уровень')
    use_time = models.CharField(max_length=40, verbose_name='Время накладывания')
    distant = models.FloatField(verbose_name='Дистанция')
    components = models.TextField(blank=True, verbose_name='Компоненты')
    duration = models.CharField(max_length=40, verbose_name='Длительность')
    description = models.TextField(verbose_name='описание', blank=True)
    higher_level_description = models.TextField(verbose_name='При повышении уровня', blank=True)

    class Meta:
        verbose_name = 'Заклинание'
        verbose_name_plural = 'Заклинания'

    def __str__(self):
        return self.name


class Damage(models.Model):
    # FIXME не уверен, что тут PROTECT
    #  думаю, тут достаточно было бы CASCADE, т.к. если ты удаляешь главный объект (мало ли)
    #  то хотел бы, чтобы была не ошибка, а всё удалилось вместе.
    #  Во всяком случае, я PROTECT встречал редко и тут не похоже на кейс, где он нужен
    damage_dice = models.ForeignKey('Dices', on_delete=models.PROTECT, verbose_name='Кость урона')
    dice_quantity = models.IntegerField(verbose_name='Количество костей')
    damage_type = models.ForeignKey('DamageTypes', on_delete=models.PROTECT, verbose_name='Тип урона')


class DamageOnLevel(Damage, models.Model):
    level = models.IntegerField(verbose_name='Уровень')


class DamageSpells(Spells, models.Model):
    damage = models.ManyToManyField('Damage', verbose_name='Урон')
    for_level_update_damage = models.ManyToManyField('Damage', verbose_name='Увеличение урона',
                                                     related_name='damage_to_spell_level', blank=True)
    on_hero_levels_damage_changes = models.ManyToManyField('DamageOnLevel', verbose_name='Урон от уровня персонажа',
                                                           related_name='damage_to_char_level', blank=True)

    class Meta:
        verbose_name = 'Заклинание с уроном'
        verbose_name_plural = 'Заклинания с уроном'
