from django.contrib import admin

from academics.models import (Country, CountryDraft,
                              Course, CourseDraft,
                              Currency, CurrencyDraft,
                              DegreeType, DegreeTypeDraft,
                              Discipline, DisciplineDraft,
                              Language, LanguageDraft,
                              School, SchoolDraft,
                              ProgrammeType)


admin.site.register(Country)
admin.site.register(CountryDraft)

admin.site.register(Course)
admin.site.register(CourseDraft)

admin.site.register(Currency)
admin.site.register(CurrencyDraft)

admin.site.register(DegreeType)
admin.site.register(DegreeTypeDraft)

admin.site.register(Discipline)
admin.site.register(DisciplineDraft)

admin.site.register(Language)
admin.site.register(LanguageDraft)

admin.site.register(School)
admin.site.register(SchoolDraft)

admin.site.register(ProgrammeType)