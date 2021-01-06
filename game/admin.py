from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from game.admin_pre_filtered_list_filter import PreFilteredListFilter
from game.constants import QUESTIONS_PER_GAME
from game.models import AppUser, AppGroup, Question, Game


class GameInlineAdmin(admin.StackedInline):
    model = Game
    fields = ("points", "created_at")
    readonly_fields = ("created_at",)
    extra = 0
    show_change_link = True


@admin.register(AppUser)
class AppUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Personal info"),
            {"fields": ("first_name", "last_name", "email", "vk_id", "score")},
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ("__str__", "score", "last_login", "date_joined")
    inlines = (GameInlineAdmin,)
    ordering = ("-date_joined",)


# Move Group to the same app as User
admin.site.unregister(Group)
admin.site.register(AppGroup, GroupAdmin)


class VisibilityFilter(PreFilteredListFilter):
    default_value = True
    title = "Visible"
    parameter_name = "visible"

    def get_lookups(self):
        return [
            (True, "True"),
            (False, "False"),
        ]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    fields = (
        "question_word",
        "answer_words",
        "correct_answer",
        "selected_answer",
        "is_correct",
    )
    readonly_fields = ("is_correct",)
    list_display = (
        "id",
        "question_word",
        "correct_answer",
        "selected_answer",
        "is_correct",
    )
    ordering = ("-id",)


class QuestionInlineAdmin(admin.StackedInline):
    model = Question
    fields = (
        "question_word",
        "answer_words",
        "correct_answer",
        "selected_answer",
        "is_correct",
    )
    readonly_fields = ("is_correct",)

    def get_min_num(self, request, obj: Game = None, **kwargs):
        return QUESTIONS_PER_GAME

    def get_max_num(self, request, obj: Game = None, **kwargs):
        return QUESTIONS_PER_GAME


class CompletedGamesFilter(admin.SimpleListFilter):
    title = "Завершенные"
    parameter_name = "completed"

    def lookups(self, request, model_admin):
        return (
            ("1", "Да"),
            ("0", "Нет"),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            if int(value):
                return queryset.filter(points__gt=0)
            return queryset.filter(points=0)


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at",)
    inlines = (QuestionInlineAdmin,)
    list_display = (
        "id",
        "player",
        "points",
        "created_at",
    )
    list_filter = ("player", CompletedGamesFilter, "created_at")
    ordering = ("-created_at",)
