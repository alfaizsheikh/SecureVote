from django.contrib import admin
from .models import UserProfile, OTPVerification, Survey, SurveyOption, Vote

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'mobile_number', 'is_mobile_verified', 'created_at']
    list_filter = ['is_mobile_verified', 'created_at']
    search_fields = ['user__first_name', 'user__last_name', 'mobile_number']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(OTPVerification)
class OTPVerificationAdmin(admin.ModelAdmin):
    list_display = ['mobile_number', 'otp_code', 'is_verified', 'created_at', 'expires_at']
    list_filter = ['is_verified', 'created_at']
    search_fields = ['mobile_number']
    readonly_fields = ['created_at']

class SurveyOptionInline(admin.TabularInline):
    model = SurveyOption
    extra = 2
    fields = ['option_text', 'order']

@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_by', 'is_active', 'created_at', 'end_date']
    list_filter = ['is_active', 'created_at', 'created_by']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [SurveyOptionInline]
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new survey
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['survey', 'option', 'user_profile', 'voted_at']
    list_filter = ['survey', 'voted_at']
    search_fields = ['survey__title', 'user_profile__user__first_name', 'user_profile__mobile_number']
    readonly_fields = ['voted_at']

