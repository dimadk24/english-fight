from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from game.admin_pre_filtered_list_filter import PreFilteredListFilter
from game.constants import QUESTIONS_PER_GAME
from game.models import AppUser, AppGroup, Word, LanguagePair, Question, Game


@admin.register(AppUser)
class AppUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'),
         {'fields': ('first_name', 'last_name', 'email', 'vk_id', 'score')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups',
                       'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('__str__', 'email', 'first_name', 'last_name', 'is_staff')


# Move Group to the same app as User
admin.site.unregister(Group)
admin.site.register(AppGroup, GroupAdmin)


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    search_fields = ('text',)


class VisibilityFilter(PreFilteredListFilter):
    default_value = True
    title = 'Visible'
    parameter_name = 'visible'

    def get_lookups(self):
        return [
            (True, 'True'),
            (False, 'False'),
        ]


@admin.register(LanguagePair)
class LanguagePairAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)
    autocomplete_fields = ('english_word', 'russian_word')
    list_filter = (VisibilityFilter,)
    search_fields = ('english_word__text', 'russian_word__text')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    autocomplete_fields = (
        'question_word',
        'answer_words',
        'correct_answer',
        'selected_answer',
    )
    fields = (
        'question_word',
        'answer_words',
        'correct_answer',
        'selected_answer',
        'is_correct',
    )
    readonly_fields = ('is_correct',)


class QuestionInlineAdmin(admin.StackedInline):
    model = Question
    autocomplete_fields = (
        'question_word',
        'answer_words',
        'correct_answer',
        'selected_answer',
    )
    fields = (
        'question_word',
        'answer_words',
        'correct_answer',
        'selected_answer',
        'is_correct',
    )
    readonly_fields = ('is_correct',)

    def get_min_num(self, request, obj: Game = None, **kwargs):
        return QUESTIONS_PER_GAME

    def get_max_num(self, request, obj: Game = None, **kwargs):
        return QUESTIONS_PER_GAME


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)
    inlines = (QuestionInlineAdmin,)
