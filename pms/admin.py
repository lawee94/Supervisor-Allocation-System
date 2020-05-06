from django.contrib import admin
from pms.models import Student, Supervisor, SupervisorPreference, EligibleStudent, Test, Test2


admin.site.register(SupervisorPreference)
admin.site.register(EligibleStudent)
admin.site.register(Test)
admin.site.register(Test2)

@admin.register(Student)
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('matricNo',)}

@admin.register(Supervisor)
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('surname',)}
    
