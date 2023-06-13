from rest_framework.serializers import ValidationError

from academics.models import Course, School, Country, Currency, DegreeType, Discipline, Language
from academics.serializers import DetailCourseSerializer, DetailSchoolSerializer, DetailCountrySerializer, DetailCurrencySerializer, DetailDegreeTypeSerializer, DetailDisciplineSerializer, DetailLanguageSerializer

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
        course_object = Course.objects.get(pk=self.data["id"])
        course = DetailCourseSerializer(course_object)
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
        course_object = Course.objects.get(pk=self.data["id"])
        course = DetailCourseSerializer(course_object)
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
        course_object = Course.objects.get(pk=self.data["id"])
        course = DetailCourseSerializer(course_object)
        title = f"Published: {course.data['name']}"
        detail = f"The course entry: {course.data['name']} has been published.\n\nEntry:\n"
        for item, i in zip(course.data, range(len(course.data))):
            detail += f"{i+1}. {item}: {course.data[item]}\n"
        
        return {
            "type": Notification.PUBLISH,
            "title": title,
            "detail": detail
        }


class SchoolPublishNotification(EntryPublishNotification):

    def compose_notification(self):
        school_object = School.objects.get(pk=self.data["id"])
        school = DetailSchoolSerializer(school_object)
        title = f"Published: {school.data['name']}"
        detail = f"Your school entry: {school.data['name']} has been published.\n\nEntry:\n"
        for item, i in zip(school.data, range(len(school.data))):
            detail += f"{i+1}. {item}: {school.data[item]}\n"
        
        return {
            "type": Notification.PUBLISH,
            "title": title,
            "detail": detail
        }
    

class SupervisorSchoolPublishNotification(EntryPublishNotification):

    def compose_notification(self):
        school_object = School.objects.get(pk=self.data["id"])
        school = DetailSchoolSerializer(school_object)
        title = f"Published: {school.data['name']}"
        detail = f"The school entry: {school.data['name']} has been published.\n\nEntry:\n"
        for item, i in zip(school.data, range(len(school.data))):
            detail += f"{i+1}. {item}: {school.data[item]}\n"
        
        return {
            "type": Notification.PUBLISH,
            "title": title,
            "detail": detail
        }
    

class AdminSchoolPublishNotification(EntryPublishNotification):

    def compose_notification(self):
        school_object = School.objects.get(pk=self.data["id"])
        school = DetailSchoolSerializer(school_object)
        title = f"Published: {school.data['name']}"
        detail = f"The school entry: {school.data['name']} has been published.\n\nEntry:\n"
        for item, i in zip(school.data, range(len(school.data))):
            detail += f"{i+1}. {item}: {school.data[item]}\n"
        
        return {
            "type": Notification.PUBLISH,
            "title": title,
            "detail": detail
        }


class CountryPublishNotification(EntryPublishNotification):
    """
        TODO: Just create a single notification that should be broadcast to all staff users
    """

    def compose_notification(self):
        country_object = Country.objects.get(pk=self.data["id"])
        country = DetailCountrySerializer(country_object)
        title = f"Published: {country.data['name']}"
        detail = f"Your country entry: {country.data['name']} has been published.\n\nEntry:\n"
        for item, i in zip(country.data, range(len(country.data))):
            detail += f"{i+1}. {item}: {country.data[item]}\n"
        
        return {
            "type": Notification.PUBLISH,
            "title": title,
            "detail": detail
        }
    

class SupervisorCountryPublishNotification(EntryPublishNotification):

    def compose_notification(self):
        country_object = Country.objects.get(pk=self.data["id"])
        country = DetailCountrySerializer(country_object)
        title = f"Published: {country.data['name']}"
        detail = f"The country entry: {country.data['name']} has been published.\n\nEntry:\n"
        for item, i in zip(country.data, range(len(country.data))):
            detail += f"{i+1}. {item}: {country.data[item]}\n"
        
        return {
            "type": Notification.PUBLISH,
            "title": title,
            "detail": detail
        }
    

class AdminCountryPublishNotification(EntryPublishNotification):

    def compose_notification(self):
        country_object = Country.objects.get(pk=self.data["id"])
        country = DetailCountrySerializer(country_object)
        title = f"Published: {country.data['name']}"
        detail = f"The country entry: {country.data['name']} has been published.\n\nEntry:\n"
        for item, i in zip(country.data, range(len(country.data))):
            detail += f"{i+1}. {item}: {country.data[item]}\n"
        
        return {
            "type": Notification.PUBLISH,
            "title": title,
            "detail": detail
        }
    

class CurrencyPublishNotification(EntryPublishNotification):
    """
        TODO: Just create a single notification that should be broadcast to all staff users
    """
    
    def compose_notification(self):
        currency_object = Currency.objects.get(pk=self.data["id"])
        currency = DetailCurrencySerializer(currency_object)
        title = f"Published: {currency.data['name']}"
        detail = f"Your currency entry: {currency.data['name']} has been published.\n\nEntry:\n"
        for item, i in zip(currency.data, range(len(currency.data))):
            detail += f"{i+1}. {item}: {currency.data[item]}\n"
        
        return {
            "type": Notification.PUBLISH,
            "title": title,
            "detail": detail
        }
    

class SupervisorCurrencyPublishNotification(EntryPublishNotification):

    def compose_notification(self):
        currency_object = Currency.objects.get(pk=self.data["id"])
        currency = DetailCurrencySerializer(currency_object)
        title = f"Published: {currency.data['name']}"
        detail = f"The currency entry: {currency.data['name']} has been published.\n\nEntry:\n"
        for item, i in zip(currency.data, range(len(currency.data))):
            detail += f"{i+1}. {item}: {currency.data[item]}\n"
        
        return {
            "type": Notification.PUBLISH,
            "title": title,
            "detail": detail
        }
    

class AdminCurrencyPublishNotification(EntryPublishNotification):

    def compose_notification(self):
        currency_object = Currency.objects.get(pk=self.data["id"])
        currency = DetailCurrencySerializer(currency_object)
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
    

class DisciplinePublishNotification(EntryPublishNotification):
    """
        TODO: Just create a single notification that should be broadcast to all staff users
    """
    
    def compose_notification(self):
        discipline_object = Discipline.objects.get(pk=self.data["id"])
        discipline = DetailDisciplineSerializer(discipline_object)
        title = f"Published: {discipline.data['name']}"
        detail = f"Your discipline entry: {discipline.data['name']} has been published.\n\nEntry:\n"
        for item, i in zip(discipline.data, range(len(discipline.data))):
            detail += f"{i+1}. {item}: {discipline.data[item]}\n"
        
        return {
            "type": Notification.PUBLISH,
            "title": title,
            "detail": detail
        }
    

class SupervisorDisciplinePublishNotification(EntryPublishNotification):

    def compose_notification(self):
        discipline_object = Discipline.objects.get(pk=self.data["id"])
        discipline = DetailDisciplineSerializer(discipline_object)
        title = f"Published: {discipline.data['name']}"
        detail = f"The discipline entry: {discipline.data['name']} has been published.\n\nEntry:\n"
        for item, i in zip(discipline.data, range(len(discipline.data))):
            detail += f"{i+1}. {item}: {discipline.data[item]}\n"
        
        return {
            "type": Notification.PUBLISH,
            "title": title,
            "detail": detail
        }
    

class AdminDisciplinePublishNotification(EntryPublishNotification):

    def compose_notification(self):
        discipline_object = Discipline.objects.get(pk=self.data["id"])
        discipline = DetailDisciplineSerializer(discipline_object)
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

