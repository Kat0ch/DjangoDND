from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from .models import *
from .forms import *
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import login, logout


def auto_filter(parameters: dict[str:str],
                form) -> Q:
    queryset_filter: Q = Q()
    for parameter in parameters:
        parameter_value: dict = form.cleaned_data.get(parameter)
        if parameter_value:
            if parameters[parameter] == 'Char':
                queryset_filter &= Q(**{f'{parameter}__icontains': parameter_value})
            elif parameters[parameter] == 'MMCF':
                queryset_filter &= Q(**{f'{parameter}__in': parameter_value})
            elif parameters[parameter] == 'Num':
                queryset_filter &= Q(**{f'{parameter}': parameter_value})

    return queryset_filter


def register(request):
    if request.method == 'POST':
        form: RegistrationForm = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form: RegistrationForm = RegistrationForm()
    return render(request, 'playersbook/register.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'playersbook/login.html', {'form': form})


class HomePB(ListView):
    model = Classes
    template_name: str = 'playersbook/home.html'
    context_object_name: str = 'classes'


class ClassView(ListView):
    model = Classes
    template_name: str = 'playersbook/class_view.html'
    context_object_name: str = 'class'

    def get_queryset(self):
        return Classes.objects.get(pk=self.kwargs['class_id'])


class ClassesList(ListView):
    model = Classes
    template_name: str = 'playersbook/class_list.html'
    context_object_name: str = 'classes'

    def get_queryset(self):
        queryset = super().get_queryset()
        form = ClassesFilterForm(self.request.GET)

        classes_filter: Q = Q()

        if form.is_valid():
            parameters: dict[str: str] = {'name': 'Char',
                                          'main_chars': 'MMCF',
                                          'hit_dice': 'MMCF',
                                          'saving_throws': 'MMCF',
                                          }
            classes_filter &= auto_filter(parameters, form)
            if form.cleaned_data.get('spells'):
                classes_filter &= ~Q(spells__isnull=form.cleaned_data.get('spells'))

        return queryset.filter(classes_filter)

    def get_context_data(self,
                         *,
                         object_list=None,
                         **kwargs) -> dict:
        context: dict = super().get_context_data()
        context['form'] = ClassesFilterForm(self.request.GET)

        return context


class SpellsBySource(ListView):
    model = Items
    template_name: str = 'playersbook/spells_list.html'
    context_object_name: str = 'spells'

    def get_queryset(self):
        return Items.objects.filter(source_id=self.kwargs['source_id']).select_related('source')


class WeaponsList(ListView):
    template_name: str = 'playersbook/weapons_list.html'
    context_object_name: str = 'weapons'
    model = Weapons

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        context: dict = super().get_context_data(**kwargs)
        context['form'] = WeaponsFilterForm()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form: WeaponsFilterForm = WeaponsFilterForm(self.request.GET)
        parameters: dict[str: str] = dict()
        if form.is_valid():
            parameters = {'name': 'Char',
                          'weapon_class': 'MMCF',
                          'category': 'MMCF',
                          'features': 'MMCF',
                          'technique': 'MMCF',
                          'damage_type': 'MMCF'}

        return queryset.filter(auto_filter(parameters, form))


class ArmorsList(ListView):
    template_name: str = 'playersbook/armors_list.html'
    context_object_name: str = 'armors'
    model = Armors

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        context: dict = super().get_context_data(**kwargs)
        context['form'] = ArmorsFilterForm()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form: ArmorsFilterForm = ArmorsFilterForm(self.request.GET)

        armors_filter: Q = Q()
        if form.is_valid():
            parameters: dict[str: str] = {'name': 'Char',
                                          'category': 'MMCF',
                                          }
            if form.is_valid():
                armors_filter = auto_filter(parameters, form)
                if form.cleaned_data.get('min_AC'):
                    armors_filter &= Q(AC__gt=form.cleaned_data.get('min_AC'))
                if form.cleaned_data.get('max_AC'):
                    armors_filter &= Q(AC__lt=form.cleaned_data.get('max_AC'))
                if form.cleaned_data.get('strength'):
                    armors_filter &= Q(strength__isnull=form.cleaned_data.get('strength'))
                if form.cleaned_data.get('stealth'):
                    armors_filter &= ~Q(stealth=form.cleaned_data.get('stealth'))

        return queryset.filter(armors_filter).order_by('category')


class ItemsList(ListView):
    template_name: str = 'playersbook/items_list.html'
    context_object_name: str = 'items'
    model = Items

    def get_context_data(self, *, object_list=None, clear_form: bool = False, **kwargs) -> dict:
        context: dict = super().get_context_data(**kwargs)
        if not clear_form:
            context['form'] = ItemsFilterForm(self.request.GET)
        else:
            context['form'] = ItemsFilterForm()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form: ItemsFilterForm = ItemsFilterForm(self.request.GET)
        items_filter: Q = Q()

        if form.is_valid():
            parameters: dict[str: str] = {'name': 'Char',
                                          'source': 'MMCF'}
            items_filter &= auto_filter(parameters, form)
            if form.cleaned_data.get('max_price'):
                items_filter &= Q(price__lt=form.cleaned_data.get('max_price'))
            if form.cleaned_data.get('min_price'):
                items_filter &= Q(price__gt=form.cleaned_data.get('min_price'))
        return queryset.filter(items_filter)


class SubclassByClassView(ListView):
    template_name: str = 'playersbook/subclasses_by_class.html'
    context_object_name: str = 'subclasses'
    model = SubClasses

    def get_queryset(self):
        classes = Classes.objects.get(pk=self.kwargs['class_id'])
        return classes.sub_classes

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        context: dict = super().get_context_data(**kwargs)
        context['class_id'] = self.kwargs['class_id']
        context['class'] = Classes.objects.get(pk=self.kwargs['class_id'])
        return context


class SpellsByClassesView(ListView):
    template_name: str = 'playersbook/classes_spells.html'
    context_object_name: str = 'class'
    model = Classes

    def get_queryset(self):
        return Classes.objects.get(pk=self.kwargs['class_id'])
