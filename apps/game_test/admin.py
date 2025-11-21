from django.contrib import admin
from .models import Level, Question, AnswerOption, UserLevelResult


# --- INLINE для ответов ---
class AnswerOptionInline(admin.TabularInline):
    model = AnswerOption
    extra = 2
    fields = ("text", "is_correct")
    classes = ["collapse"]


# --- Вопросы можно открывать через inline внутри уровня ---
class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1
    show_change_link = True


# --- ADMIN: Уровни ---
@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ("number", "name")
    ordering = ("number",)
    search_fields = ("number", "name")
    inlines = [QuestionInline]


# --- ADMIN: Вопросы ---
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("text", "level")
    list_filter = ("level",)
    search_fields = ("text",)
    inlines = [AnswerOptionInline]


# --- ADMIN: Варианты ответов ---
@admin.register(AnswerOption)
class AnswerOptionAdmin(admin.ModelAdmin):
    list_display = ("text", "question", "is_correct")
    list_filter = ("is_correct", "question__level")
    search_fields = ("text",)
    list_editable = ("is_correct",)


# --- ADMIN: Результаты пользователя ---
@admin.register(UserLevelResult)
class UserLevelResultAdmin(admin.ModelAdmin):
    list_display = ("user", "level", "score", "stars", "created_at")
    list_filter = ("level", "stars", "created_at")
    search_fields = ("user__username", "user__phone_number")
    readonly_fields = ("score", "stars", "created_at")  # ❗ чтобы нельзя было редактировать вручную
    ordering = ("-created_at",)
