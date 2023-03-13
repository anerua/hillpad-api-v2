from django.contrib import admin

from academics.models import Country, School, Discipline, Currency, ProgrammeType, DegreeType, CourseDates, Language, Course


admin.site.register(Country)
admin.site.register(School)
admin.site.register(Discipline)
admin.site.register(Currency)
admin.site.register(ProgrammeType)
admin.site.register(DegreeType)
admin.site.register(CourseDates)
admin.site.register(Language)
admin.site.register(Course)