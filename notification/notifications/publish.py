from rest_framework.serializers import ValidationError

from academics.models import CourseDraft, SchoolDraft, CountryDraft, CurrencyDraft, DegreeType, DisciplineDraft, Language
from academics.serializers import DetailCourseDraftSerializer, DetailSchoolDraftSerializer, DetailCountryDraftSerializer, DetailCurrencyDraftSerializer, DetailDegreeTypeSerializer, DetailDisciplineDraftSerializer, DetailLanguageSerializer

from notification.models import Notification
from notification.serializers import CreateNotificationSerializer


class EntryPublishNotification():

    def __init__(self, data):
        self.data = data

    def create_notification(self):
        notification_data = self.compose_notification()
        serializer = CreateNotificationSerializer(data=notification_data)
        if serializer.is_valid():
            serializer.save()
            return serializer.data
        
        raise ValidationError(serializer.errors)

    def compose_notification(self): ...


class CourseDraftPublishNotification(EntryPublishNotification):

    def compose_notification(self):
        course_object = CourseDraft.objects.get(pk=self.data["id"])
        course = DetailCourseDraftSerializer(course_object)
        title = f"Published: {course.data['name']}"
        detail = f"Your course entry: {course.data['name']} has been published.\n\nEntry:\n"
        for item, i in zip(course.data, range(len(course.data))):
            detail += f"{i+1}. {item}: {course.data[item]}\n"
        
        return {
            "type": Notification.PUBLISH,
            "title": title,
            "detail": detail
        }
    

class SupervisorCourseDraftPublishNotification(EntryPublishNotification):

    def compose_notification(self):
        course_object = CourseDraft.objects.get(pk=self.data["id"])
        course = DetailCourseDraftSerializer(course_object)
        title = f"Published: {course.data['name']}"
        detail = f"The course entry: {course.data['name']} has been published.\n\nEntry:\n"
        for item, i in zip(course.data, range(len(course.data))):
            detail += f"{i+1}. {item}: {course.data[item]}\n"
        
        return {
            "type": Notification.PUBLISH,
            "title": title,
            "detail": detail
        }
    

class AdminCourseDraftPublishNotification(EntryPublishNotification):

    def compose_notification(self):
        course_object = CourseDraft.objects.get(pk=self.data["id"])
        course = DetailCourseDraftSerializer(course_object)
        title = f"Published: {course.data['name']}"
        detail = f"The course entry: {course.data['name']} has been published.\n\nEntry:\n"
        for item, i in zip(course.data, range(len(course.data))):
            detail += f"{i+1}. {item}: {course.data[item]}\n"
        
        return {
            "type": Notification.PUBLISH,
            "title": title,
            "detail": detail
        }


class SchoolDraftPublishNotification(EntryPublishNotification):

    def compose_notification(self):
        school_object = SchoolDraft.objects.get(pk=self.data["id"])
        school = DetailSchoolDraftSerializer(school_object)
        title = f"Published: {school.data['name']}"
        detail = f"Your school entry: {school.data['name']} has been published.\n\nEntry:\n"
        for item, i in zip(school.data, range(len(school.data))):
            detail += f"{i+1}. {item}: {school.data[item]}\n"
        
        return {
            "type": Notification.PUBLISH,
            "title": title,
            "detail": detail
        }
    

class SupervisorSchoolDraftPublishNotification(EntryPublishNotification):

    def compose_notification(self):
        school_object = SchoolDraft.objects.get(pk=self.data["id"])
        school = DetailSchoolDraftSerializer(school_object)
        title = f"Published: {school.data['name']}"
        detail = f"The school entry: {school.data['name']} has been published.\n\nEntry:\n"
        for item, i in zip(school.data, range(len(school.data))):
            detail += f"{i+1}. {item}: {school.data[item]}\n"
        
        return {
            "type": Notification.PUBLISH,
            "title": title,
            "detail": detail
        }
    

class AdminSchoolDraftPublishNotification(EntryPublishNotification):

    def compose_notification(self):
        school_object = SchoolDraft.objects.get(pk=self.data["id"])
        school = DetailSchoolDraftSerializer(school_object)
        title = f"Published: {school.data['name']}"
        detail = f"The school entry: {school.data['name']} has been published.\n\nEntry:\n"
        for item, i in zip(school.data, range(len(school.data))):
            detail += f"{i+1}. {item}: {school.data[item]}\n"
        
        return {
            "type": Notification.PUBLISH,
            "title": title,
            "detail": detail
        }


class CountryDraftPublishNotification(EntryPublishNotification):
    """
        TODO: Just create a single notification that should be broadcast to all staff users
    """

    def compose_notification(self):
        country_object = CountryDraft.objects.get(pk=self.data["id"])
        country = DetailCountryDraftSerializer(country_object)
        title = f"Published: {country.data['name']}"
        detail = f"Your country entry: {country.data['name']} has been published.\n\nEntry:\n"
        for item, i in zip(country.data, range(len(country.data))):
            detail += f"{i+1}. {item}: {country.data[item]}\n"
        
        return {
            "type": Notification.PUBLISH,
            "title": title,
            "detail": detail
        }
    

class SupervisorCountryDraftPublishNotification(EntryPublishNotification):

    def compose_notification(self):
        country_object = CountryDraft.objects.get(pk=self.data["id"])
        country = DetailCountryDraftSerializer(country_object)
        title = f"Published: {country.data['name']}"
        detail = f"The country entry: {country.data['name']} has been published.\n\nEntry:\n"
        for item, i in zip(country.data, range(len(country.data))):
            detail += f"{i+1}. {item}: {country.data[item]}\n"
        
        return {
            "type": Notification.PUBLISH,
            "title": title,
            "detail": detail
        }
    

class AdminCountryDraftPublishNotification(EntryPublishNotification):

    def compose_notification(self):
        country_object = CountryDraft.objects.get(pk=self.data["id"])
        country = DetailCountryDraftSerializer(country_object)
        title = f"Published: {country.data['name']}"
        detail = f"The country entry: {country.data['name']} has been published.\n\nEntry:\n"
        for item, i in zip(country.data, range(len(country.data))):
            detail += f"{i+1}. {item}: {country.data[item]}\n"
        
        return {
            "type": Notification.PUBLISH,
            "title": title,
            "detail": detail
        }
    

class CurrencyDraftPublishNotification(EntryPublishNotification):
    """
        TODO: Just create a single notification that should be broadcast to all staff users
    """
    
    def compose_notification(self):
        currency_object = CurrencyDraft.objects.get(pk=self.data["id"])
        currency = DetailCurrencyDraftSerializer(currency_object)
        title = f"Published: {currency.data['name']}"
        detail = f"Your currency entry: {currency.data['name']} has been published.\n\nEntry:\n"
        for item, i in zip(currency.data, range(len(currency.data))):
            detail += f"{i+1}. {item}: {currency.data[item]}\n"
        
        return {
            "type": Notification.PUBLISH,
            "title": title,
            "detail": detail
        }
    

class SupervisorCurrencyDraftPublishNotification(EntryPublishNotification):

    def compose_notification(self):
        currency_object = CurrencyDraft.objects.get(pk=self.data["id"])
        currency = DetailCurrencyDraftSerializer(currency_object)
        title = f"Published: {currency.data['name']}"
        detail = f"The currency entry: {currency.data['name']} has been published.\n\nEntry:\n"
        for item, i in zip(currency.data, range(len(currency.data))):
            detail += f"{i+1}. {item}: {currency.data[item]}\n"
        
        return {
            "type": Notification.PUBLISH,
            "title": title,
            "detail": detail
        }
    

class AdminCurrencyDraftPublishNotification(EntryPublishNotification):

    def compose_notification(self):
        currency_object = CurrencyDraft.objects.get(pk=self.data["id"])
        currency = DetailCurrencyDraftSerializer(currency_object)
        title = f"Published: {currency.data['name']}"
        detail = f"The currency entry: {currency.data['name']} has been published.\n\nEntry:\n"
        for item, i in zip(currency.data, range(len(currency.data))):
            detail += f"{i+1}. {item}: {currency.data[item]}\n"
        
        return {
            "type": Notification.PUBLISH,
            "title": title,
            "detail": detail
        }


class DegreeTypePublishNotification(EntryPublishNotification):
    """
        TODO: Just create a single notification that should be broadcast to all staff users
    """
    
    def compose_notification(self):
        degree_type_object = DegreeType.objects.get(pk=self.data["id"])
        degree_type = DetailDegreeTypeSerializer(degree_type_object)
        title = f"Published: {degree_type.data['name']}"
        detail = f"Your degree_type entry: {degree_type.data['name']} has been published.\n\nEntry:\n"
        for item, i in zip(degree_type.data, range(len(degree_type.data))):
            detail += f"{i+1}. {item}: {degree_type.data[item]}\n"
        
        return {
            "type": Notification.PUBLISH,
            "title": title,
            "detail": detail
        }
    

class SupervisorDegreeTypePublishNotification(EntryPublishNotification):

    def compose_notification(self):
        degree_type_object = DegreeType.objects.get(pk=self.data["id"])
        degree_type = DetailDegreeTypeSerializer(degree_type_object)
        title = f"Published: {degree_type.data['name']}"
        detail = f"The degree_type entry: {degree_type.data['name']} has been published.\n\nEntry:\n"
        for item, i in zip(degree_type.data, range(len(degree_type.data))):
            detail += f"{i+1}. {item}: {degree_type.data[item]}\n"
        
        return {
            "type": Notification.PUBLISH,
            "title": title,
            "detail": detail
        }
    

class AdminDegreeTypePublishNotification(EntryPublishNotification):

    def compose_notification(self):
        degree_type_object = DegreeType.objects.get(pk=self.data["id"])
        degree_type = DetailDegreeTypeSerializer(degree_type_object)
        title = f"Published: {degree_type.data['name']}"
        detail = f"The degree_type entry: {degree_type.data['name']} has been published.\n\nEntry:\n"
        for item, i in zip(degree_type.data, range(len(degree_type.data))):
            detail += f"{i+1}. {item}: {degree_type.data[item]}\n"
        
        return {
            "type": Notification.PUBLISH,
            "title": title,
            "detail": detail
        }
    

class DisciplineDraftPublishNotification(EntryPublishNotification):
    """
        TODO: Just create a single notification that should be broadcast to all staff users
    """
    
    def compose_notification(self):
        discipline_object = DisciplineDraft.objects.get(pk=self.data["id"])
        discipline = DetailDisciplineDraftSerializer(discipline_object)
        title = f"Published: {discipline.data['name']}"
        detail = f"Your discipline entry: {discipline.data['name']} has been published.\n\nEntry:\n"
        for item, i in zip(discipline.data, range(len(discipline.data))):
            detail += f"{i+1}. {item}: {discipline.data[item]}\n"
        
        return {
            "type": Notification.PUBLISH,
            "title": title,
            "detail": detail
        }
    

class SupervisorDisciplineDraftPublishNotification(EntryPublishNotification):

    def compose_notification(self):
        discipline_object = DisciplineDraft.objects.get(pk=self.data["id"])
        discipline = DetailDisciplineDraftSerializer(discipline_object)
        title = f"Published: {discipline.data['name']}"
        detail = f"The discipline entry: {discipline.data['name']} has been published.\n\nEntry:\n"
        for item, i in zip(discipline.data, range(len(discipline.data))):
            detail += f"{i+1}. {item}: {discipline.data[item]}\n"
        
        return {
            "type": Notification.PUBLISH,
            "title": title,
            "detail": detail
        }
    

class AdminDisciplineDraftPublishNotification(EntryPublishNotification):

    def compose_notification(self):
        discipline_object = DisciplineDraft.objects.get(pk=self.data["id"])
        discipline = DetailDisciplineDraftSerializer(discipline_object)
        title = f"Published: {discipline.data['name']}"
        detail = f"The discipline entry: {discipline.data['name']} has been published.\n\nEntry:\n"
        for item, i in zip(discipline.data, range(len(discipline.data))):
            detail += f"{i+1}. {item}: {discipline.data[item]}\n"
        
        return {
            "type": Notification.PUBLISH,
            "title": title,
            "detail": detail
        }


class LanguagePublishNotification(EntryPublishNotification):
    """
        TODO: Just create a single notification that should be broadcast to all staff users
    """
    
    def compose_notification(self):
        language_object = Language.objects.get(pk=self.data["id"])
        language = DetailLanguageSerializer(language_object)
        title = f"Published: {language.data['name']}"
        detail = f"Your language entry: {language.data['name']} has been published.\n\nEntry:\n"
        for item, i in zip(language.data, range(len(language.data))):
            detail += f"{i+1}. {item}: {language.data[item]}\n"
        
        return {
            "type": Notification.PUBLISH,
            "title": title,
            "detail": detail
        }
    

class SupervisorLanguagePublishNotification(EntryPublishNotification):

    def compose_notification(self):
        language_object = Language.objects.get(pk=self.data["id"])
        language = DetailLanguageSerializer(language_object)
        title = f"Published: {language.data['name']}"
        detail = f"The language entry: {language.data['name']} has been published.\n\nEntry:\n"
        for item, i in zip(language.data, range(len(language.data))):
            detail += f"{i+1}. {item}: {language.data[item]}\n"
        
        return {
            "type": Notification.PUBLISH,
            "title": title,
            "detail": detail
        }
    

class AdminLanguagePublishNotification(EntryPublishNotification):

    def compose_notification(self):
        language_object = Language.objects.get(pk=self.data["id"])
        language = DetailLanguageSerializer(language_object)
        title = f"Published: {language.data['name']}"
        detail = f"The language entry: {language.data['name']} has been published.\n\nEntry:\n"
        for item, i in zip(language.data, range(len(language.data))):
            detail += f"{i+1}. {item}: {language.data[item]}\n"
        
        return {
            "type": Notification.PUBLISH,
            "title": title,
            "detail": detail
        }

