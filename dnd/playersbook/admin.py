from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


class ToolsAdmin(admin.ModelAdmin):
    pass


class ClassesAdmin(admin.ModelAdmin):
    list_display: tuple = ('id', 'name', 'hit_dice')
    list_display_links: tuple = ('id', 'name')


class SubClassesAdmin(admin.ModelAdmin):
    list_display: tuple = ('id', 'sub_class_name')
    list_display_links: tuple = ('id', 'sub_class_name')


class LevelsAdmin(admin.ModelAdmin):
    pass


class WeaponsAdmin(admin.ModelAdmin):
    pass


class ItemsAdmin(admin.ModelAdmin):
    list_display: tuple = ('id', 'name', 'price_correct_display', 'weight')

    def price_correct_display(self,
                              obj: Items):
        price: int = obj.price
        if price / 10 >= 1:
            if price / 100 >= 1:
                return mark_safe(f'{price / 100} зм')
            else:
                return mark_safe(f'{price / 10} см')
        else:
            return mark_safe(f'{price} мм')

    price_correct_display.short_description = 'Цена'


class DamageTypesAdmin(admin.ModelAdmin):
    pass


class SpellsAdmin(admin.ModelAdmin):
    pass


class DamageSpellsAdmin(admin.ModelAdmin):
    pass


class DamageAdmin(admin.ModelAdmin):
    pass


class WeaponsTechniquesAdmin(admin.ModelAdmin):
    pass


class ArmorsAdmin(admin.ModelAdmin):
    pass


class DamageOnLevelAdmin(admin.ModelAdmin):
    pass


admin.site.register(Classes, ClassesAdmin)
admin.site.register(Weapons, WeaponsAdmin)
admin.site.register(Armors, ArmorsAdmin)
admin.site.register(Items, ItemsAdmin)
admin.site.register(WeaponsTechniques, WeaponsTechniquesAdmin)
admin.site.register(DamageTypes, DamageTypesAdmin)
admin.site.register(SubClasses, SubClassesAdmin)
admin.site.register(Tools, ToolsAdmin)
admin.site.register(Levels, LevelsAdmin)
admin.site.register(Spells, SpellsAdmin)
admin.site.register(DamageSpells, DamageSpellsAdmin)
admin.site.register(Damage, DamageAdmin)
admin.site.register(DamageOnLevel, DamageOnLevelAdmin)