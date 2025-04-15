from django.urls import path
from .views import *


urlpatterns: list = [
    path('', HomePB.as_view(), name='home'),
    path('class/<int:class_id>/', ClassView.as_view(), name='class'),
    path('spells/<int:source_id>/', SpellsBySource.as_view(), name='spells_to_source'),
    path('weapons/', WeaponsList.as_view(), name='weapons'),
    path('armors/', ArmorsList.as_view(), name='armors'),
    path('items/', ItemsList.as_view(), name='items'),
    path('classes/', ClassesList.as_view(), name='classes'),
    path('class/<int:class_id>/subclasses', SubclassByClassView.as_view(), name='subclasses_by_class'),
    path('class/<int:class_id>/spells', SpellsByClassesView.as_view(), name='class_spells'),
    path('class/<int:class_id>/spells', SpellsByClassesView.as_view(), name='class_spells'),
    path('registration/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
]
