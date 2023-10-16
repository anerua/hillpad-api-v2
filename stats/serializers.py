from collections import OrderedDict
from rest_framework import serializers

from academics.models import (
        Course, CourseDraft,
        School, SchoolDraft,
        Country, CountryDraft,
        Discipline, DisciplineDraft,
        DegreeType, DegreeTypeDraft,
        Currency, CurrencyDraft,
    )


class AccountEntriesStatsSerializer(serializers.Serializer):

    metrics = serializers.ListField(
        child = serializers.CharField(),
        write_only = True
    )
    date = serializers.DateField(write_only=True, required=False)

    daily_courses_added = serializers.IntegerField(read_only=True, required=False)
    daily_bachelors_added = serializers.IntegerField(read_only=True, required=False)
    daily_masters_added = serializers.IntegerField(read_only=True, required=False)
    daily_doctorates_added = serializers.IntegerField(read_only=True, required=False)
    daily_schools_added = serializers.IntegerField(read_only=True, required=False)
    daily_countries_added = serializers.IntegerField(read_only=True, required=False)
    daily_disciplines_added = serializers.IntegerField(read_only=True, required=False)
    daily_degree_types_added = serializers.IntegerField(read_only=True, required=False)
    daily_currencies_added = serializers.IntegerField(read_only=True, required=False)

    total_courses_added = serializers.IntegerField(read_only=True, required=False)
    total_bachelors_added = serializers.IntegerField(read_only=True, required=False)
    total_masters_added = serializers.IntegerField(read_only=True, required=False)
    total_doctorates_added = serializers.IntegerField(read_only=True, required=False)
    total_schools_added = serializers.IntegerField(read_only=True, required=False)
    total_countries_added = serializers.IntegerField(read_only=True, required=False)
    total_disciplines_added = serializers.IntegerField(read_only=True, required=False)
    total_degree_types_added = serializers.IntegerField(read_only=True, required=False)
    total_currencies_added = serializers.IntegerField(read_only=True, required=False)

    total_courses_review = serializers.IntegerField(read_only=True, required=False)
    total_bachelors_review = serializers.IntegerField(read_only=True, required=False)
    total_masters_review = serializers.IntegerField(read_only=True, required=False)
    total_doctorates_review = serializers.IntegerField(read_only=True, required=False)
    total_schools_review = serializers.IntegerField(read_only=True, required=False)
    total_countries_review = serializers.IntegerField(read_only=True, required=False)
    total_disciplines_review = serializers.IntegerField(read_only=True, required=False)
    total_degree_types_review = serializers.IntegerField(read_only=True, required=False)
    total_currencies_review = serializers.IntegerField(read_only=True, required=False)

    total_courses_approved = serializers.IntegerField(read_only=True, required=False)
    total_bachelors_approved = serializers.IntegerField(read_only=True, required=False)
    total_masters_approved = serializers.IntegerField(read_only=True, required=False)
    total_doctorates_approved = serializers.IntegerField(read_only=True, required=False)
    total_schools_approved = serializers.IntegerField(read_only=True, required=False)

    total_courses_rejected = serializers.IntegerField(read_only=True, required=False)
    total_bachelors_rejected = serializers.IntegerField(read_only=True, required=False)
    total_masters_rejected = serializers.IntegerField(read_only=True, required=False)
    total_doctorates_rejected = serializers.IntegerField(read_only=True, required=False)
    total_schools_rejected = serializers.IntegerField(read_only=True, required=False)

    total_courses_published = serializers.IntegerField(read_only=True, required=False)
    total_bachelors_published = serializers.IntegerField(read_only=True, required=False)
    total_masters_published = serializers.IntegerField(read_only=True, required=False)
    total_doctorates_published = serializers.IntegerField(read_only=True, required=False)
    total_schools_published = serializers.IntegerField(read_only=True, required=False)
    total_countries_published = serializers.IntegerField(read_only=True, required=False)
    total_disciplines_published = serializers.IntegerField(read_only=True, required=False)
    total_degree_types_published = serializers.IntegerField(read_only=True, required=False)
    total_currencies_published = serializers.IntegerField(read_only=True, required=False)

    total_courses_review_db = serializers.IntegerField(read_only=True, required=False)
    total_bachelors_review_db = serializers.IntegerField(read_only=True, required=False)
    total_masters_review_db = serializers.IntegerField(read_only=True, required=False)
    total_doctorates_review_db = serializers.IntegerField(read_only=True, required=False)
    total_schools_review_db = serializers.IntegerField(read_only=True, required=False)

    total_courses_published_db = serializers.IntegerField(read_only=True, required=False)
    total_bachelors_published_db = serializers.IntegerField(read_only=True, required=False)
    total_masters_published_db = serializers.IntegerField(read_only=True, required=False)
    total_doctorates_published_db = serializers.IntegerField(read_only=True, required=False)
    total_schools_published_db = serializers.IntegerField(read_only=True, required=False)

    def validate(self, data):
        fields = [(lambda field: field.field_name)(field) for field in self._readable_fields]
        metrics = self.initial_data["metrics"]
        for metric in metrics:
            if metric not in fields:
                raise serializers.ValidationError(f"{metric} is not a valid metric.")
            if metric[:5] == "daily" and "date" not in self.initial_data:
                raise serializers.ValidationError(f"You must specify a date to get the {metric} metric")
        
        return super(AccountEntriesStatsSerializer, self).validate(data)

    def to_representation(self, instance):
        ret = OrderedDict()

        request = self.context.get("request")
        user = None
        if request and hasattr(request, "user"):
            user = request.user

        metrics = self.initial_data["metrics"]
        date = None
        if "date" in self.initial_data:
            date = self.initial_data["date"]
        else:
            date = None
        for metric in metrics:
            metric_value = self.get_value(metric, date, user)
            if metric_value is not None:
                ret[metric] = metric_value

        return ret
    
    def get_value(self, metric, date, user):
        if metric == "daily_courses_added":
            return CourseDraft.objects.filter(author=user, created_at__date=date).count()
        elif metric == "daily_bachelors_added":
            return CourseDraft.objects.filter(author=user, created_at__date=date, programme_type__name="Bachelors").count()
        elif metric == "daily_masters_added":
            return CourseDraft.objects.filter(author=user, created_at__date=date, programme_type__name="Masters").count()
        elif metric == "daily_doctorates_added":
            return CourseDraft.objects.filter(author=user, created_at__date=date, programme_type__name="Doctorates").count()
        elif metric == "daily_schools_added":
            return SchoolDraft.objects.filter(author=user, created_at__date=date).count()
        elif metric == "daily_countries_added":
            return CountryDraft.objects.filter(author=user, created_at__date=date).count()
        elif metric == "daily_disciplines_added":
            return DisciplineDraft.objects.filter(author=user, created_at__date=date).count()
        elif metric == "daily_degree_types_added":
            return DegreeTypeDraft.objects.filter(author=user, created_at__date=date).count()
        elif metric == "daily_currencies_added":
            return CurrencyDraft.objects.filter(author=user, created_at__date=date).count()

        elif metric == "total_courses_review":
            return CourseDraft.objects.filter(author=user, status=CourseDraft.REVIEW).count()
        elif metric == "total_bachelors_review":
            return CourseDraft.objects.filter(author=user, status=CourseDraft.REVIEW, programme_type__name="Bachelors").count()
        elif metric == "total_masters_review":
            return CourseDraft.objects.filter(author=user, status=CourseDraft.REVIEW, programme_type__name="Masters").count()
        elif metric == "total_doctorates_review":
            return CourseDraft.objects.filter(author=user, status=CourseDraft.REVIEW, programme_type__name="Doctorates").count()
        elif metric == "total_schools_review":
            return SchoolDraft.objects.filter(author=user, status=SchoolDraft.REVIEW).count()
        elif metric == "total_countries_review":
            return CountryDraft.objects.filter(author=user, status=CountryDraft.REVIEW).count()
        elif metric == "total_disciplines_review":
            return DisciplineDraft.objects.filter(author=user, status=DisciplineDraft.REVIEW).count()
        elif metric == "total_degree_types_review":
            return DegreeTypeDraft.objects.filter(author=user, status=DegreeTypeDraft.REVIEW).count()
        elif metric == "total_currencies_review":
            return CurrencyDraft.objects.filter(author=user, status=CurrencyDraft.REVIEW).count()

        elif metric == "total_courses_approved":
            return CourseDraft.objects.filter(author=user, status=CourseDraft.APPROVED).count()
        elif metric == "total_bachelors_approved":
            return CourseDraft.objects.filter(author=user, status=CourseDraft.APPROVED, programme_type__name="Bachelors").count()
        elif metric == "total_masters_approved":
            return CourseDraft.objects.filter(author=user, status=CourseDraft.APPROVED, programme_type__name="Masters").count()
        elif metric == "total_doctorates_approved":
            return CourseDraft.objects.filter(author=user, status=CourseDraft.APPROVED, programme_type__name="Doctorates").count()
        elif metric == "total_schools_approved":
            return SchoolDraft.objects.filter(author=user, status=SchoolDraft.APPROVED).count()
        
        elif metric == "total_courses_rejected":
            return CourseDraft.objects.filter(author=user, status=CourseDraft.REJECTED).count()
        elif metric == "total_bachelors_rejected":
            return CourseDraft.objects.filter(author=user, status=CourseDraft.REJECTED, programme_type__name="Bachelors").count()
        elif metric == "total_masters_rejected":
            return CourseDraft.objects.filter(author=user, status=CourseDraft.REJECTED, programme_type__name="Masters").count()
        elif metric == "total_doctorates_rejected":
            return CourseDraft.objects.filter(author=user, status=CourseDraft.REJECTED, programme_type__name="Doctorates").count()
        elif metric == "total_schools_rejected":
            return SchoolDraft.objects.filter(author=user, status=SchoolDraft.REJECTED).count()

        elif metric == "total_courses_published":
            return Course.objects.filter(author=user, published=True).count()
        elif metric == "total_bachelors_published":
            return Course.objects.filter(author=user, published=True, programme_type__name="Bachelors").count()
        elif metric == "total_masters_published":
            return Course.objects.filter(author=user, published=True, programme_type__name="Masters").count()
        elif metric == "total_doctorates_published":
            return Course.objects.filter(author=user, published=True, programme_type__name="Doctorates").count()
        elif metric == "total_schools_published":
            return School.objects.filter(author=user, published=True).count()
        elif metric == "total_countries_published":
            return Country.objects.filter(author=user, published=True).count()
        elif metric == "total_disciplines_published":
            return Discipline.objects.filter(author=user, published=True).count()
        elif metric == "total_degree_types_published":
            return DegreeType.objects.filter(author=user, published=True).count()
        elif metric == "total_currencies_published":
            return Currency.objects.filter(author=user, published=True).count()
        
        elif metric == "total_courses_review_db":
            return CourseDraft.objects.filter(status=CourseDraft.REVIEW).count()
        elif metric == "total_bachelors_review_db":
            return CourseDraft.objects.filter(status=CourseDraft.REVIEW, programme_type__name="Bachelors").count()
        elif metric == "total_masters_review_db":
            return CourseDraft.objects.filter(status=CourseDraft.REVIEW, programme_type__name="Masters").count()
        elif metric == "total_doctorates_review_db":
            return CourseDraft.objects.filter(status=CourseDraft.REVIEW, programme_type__name="Doctorates").count()
        elif metric == "total_schools_review_db":
            return SchoolDraft.objects.filter(status=SchoolDraft.REVIEW).count()

        elif metric == "total_courses_published_db":
            return Course.objects.filter(published=True).count()
        elif metric == "total_bachelors_published_db":
            return Course.objects.filter(published=True, programme_type__name="Bachelors").count()
        elif metric == "total_masters_published_db":
            return Course.objects.filter(published=True, programme_type__name="Masters").count()
        elif metric == "total_doctorates_published_db":
            return Course.objects.filter(published=True, programme_type__name="Doctorates").count()
        elif metric == "total_schools_published_db":
            return School.objects.filter(published=True).count()

        else:
            return None
