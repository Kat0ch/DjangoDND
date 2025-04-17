from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))

    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))

# FIXME типизацию посмотри подробнее, ты её указываешь, но не корректно
#  тут бы было что-то типа: dict[str, dict[str, bool | forms.Widget]]
#  словари аннотариуются через запятые, а не через ':'
#  ну и если уж указывать, то до конца)
filter_base_arguments: dict[str: dict[str:]] = {
    'Char': {'required': False,
             'widget': forms.TextInput(attrs={'class': 'form-control'})},
    'SM': {'required': False,
           'widget': forms.SelectMultiple(attrs={'class': 'form-select'})},
    'Num': {'required': False,
            'widget': forms.NumberInput(attrs={'class': 'form-control'})},
    'BF': {'required': False,
           'widget': forms.CheckboxInput(attrs={'class': 'form-check-input'})},
}


class RegistrationForm(UserCreationForm):
    username: forms.CharField = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1: forms.CharField = forms.CharField(label='Пароль',
                                                 widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2: forms.CharField = forms.CharField(label='Введите пароль еще раз',
                                                 widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email: forms.EmailField = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields: tuple[str] = ('username', 'email', 'password1', 'password2')
        widgets: dict[str:] = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }


class WeaponsFilterForm(forms.Form):
    model = Weapons

    name: forms.CharField = forms.CharField(
        label='Название',
        **filter_base_arguments['Char'])

    # FIXME визуально не очень нравится, что тут qs определяются в таком виде
    #  кажется, было бы правильнее делать это в инициализаторе (__init__)
    #  во всяком случае те примеры, где есть какие-то правила фильтрации (damage_type, например)
    category: forms.MultipleChoiceField = forms.ModelMultipleChoiceField(
        queryset=WeaponsCategories.objects.all(),
        label='Категории', **filter_base_arguments['SM'])

    weapon_class: forms.ModelMultipleChoiceField = forms.ModelMultipleChoiceField(
        queryset=WeaponClasses.objects.all(),
        label='Класс оружия', **filter_base_arguments['SM'])

    damage_type: forms.ModelMultipleChoiceField = forms.ModelMultipleChoiceField(
        queryset=DamageTypes.objects.filter(weapons__isnull=False).distinct(),
        label='Тип урона', **filter_base_arguments['SM'])

    features: forms.ModelMultipleChoiceField = forms.ModelMultipleChoiceField(
        queryset=WeaponsFeatures.objects.all(),
        label='Свойства оружия',
        **filter_base_arguments['SM'])

    technique: forms.ModelMultipleChoiceField = forms.ModelMultipleChoiceField(
        queryset=WeaponsTechniques.objects.all(),
        label='Оружейные приемы',
        **filter_base_arguments['SM'])


class ItemsFilterForm(forms.Form):
    model = Items

    name: forms.CharField = forms.CharField(
        label='Название',
        **filter_base_arguments['Char'])

    max_price: forms.IntegerField = forms.IntegerField(
        label='Максмальная стоимость',
        **filter_base_arguments['Num'])

    min_price: forms.IntegerField = forms.IntegerField(
        label='Минимальная стоимость',
        **filter_base_arguments['Num'])

    source: forms.ModelMultipleChoiceField = forms.ModelMultipleChoiceField(
        queryset=Sources.objects.all(),
        label='Источник', **filter_base_arguments['SM'])


class ClassesFilterForm(forms.Form):
    model = Classes
    name: forms.CharField = forms.CharField(
        label='Название',
        **filter_base_arguments['Char'])

    main_chars: forms.ModelMultipleChoiceField = forms.ModelMultipleChoiceField(
        queryset=Chars.objects.all(),
        label='Основные характеристики',
        **filter_base_arguments['SM'])

    hit_dice: forms.ModelMultipleChoiceField = forms.ModelMultipleChoiceField(
        queryset=Dices.objects.all(),
        label='Кость хитов', **filter_base_arguments['SM'])

    saving_throws: forms.ModelMultipleChoiceField = forms.ModelMultipleChoiceField(
        queryset=Chars.objects.all(),
        label='Спасброски',
        **filter_base_arguments['SM'])

    spells = forms.BooleanField(
        label='Наличие заклинаний',
        **filter_base_arguments['BF'])


class ArmorsFilterForm(forms.Form):
    model = Armors

    name: forms.CharField = forms.CharField(label='Название', **filter_base_arguments['Char'])

    category: forms.ModelMultipleChoiceField = forms.ModelMultipleChoiceField(
        queryset=ArmorCategories.objects.all(),
        label='Категория',
        **filter_base_arguments['SM'])

    min_AC: forms.IntegerField = forms.IntegerField(
        label='Минимальный КЗ',
        **filter_base_arguments['Num'])
    max_AC: forms.IntegerField = forms.IntegerField(
        label='Максимальный КЗ',
        **filter_base_arguments['Num'])

    strength: forms.IntegerField = forms.BooleanField(
        label='Без необходимости силы',
        **filter_base_arguments['BF'])

    stealth: forms.IntegerField = forms.BooleanField(
        label='Без штрафа к скрытности',
        **filter_base_arguments['BF'])
