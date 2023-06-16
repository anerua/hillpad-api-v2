from rest_framework.serializers import ValidationError

from notification.models import Notification
from notification.serializers import CreateNotificationSerializer


class EntrySubmissionNotification():

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


class CourseDraftSubmissionNotification(EntrySubmissionNotification):

    def compose_notification(self):
        title = f"Course Submission: {self.data['name']}"
        detail = f"Your course entry: {self.data['name']} has been submitted successfully and is now under review.\nEntry:\n"
        for item, i in zip(self.data, range(len(self.data))):
            detail += f"{i+1}. {item}: {self.data[item]}\n"
        
        return {
            "type": Notification.SUBMISSION,
            "title": title,
            "detail": detail
        }
    

class CourseDraftUpdateSubmissionNotification(EntrySubmissionNotification):

    def compose_notification(self):
        title = f"Course Submission (Update): {self.data['name']}"
        detail = f"An update to your course entry: {self.data['name']} has been submitted successfully and is now under review.\nEntry:\n"
        for item, i in zip(self.data, range(len(self.data))):
            detail += f"{i+1}. {item}: {self.data[item]}\n"
        
        return {
            "type": Notification.SUBMISSION,
            "title": title,
            "detail": detail
        }
    

class SchoolDraftSubmissionNotification(EntrySubmissionNotification):

    def compose_notification(self):
        title = f"School Submission: {self.data['name']}"
        detail = f"Your school entry: {self.data['name']} has been submitted successfully and is now under review.\nEntry:\n"
        for item, i in zip(self.data, range(len(self.data))):
            detail += f"{i+1}. {item}: {self.data[item]}\n"
        
        return {
            "type": Notification.SUBMISSION,
            "title": title,
            "detail": detail
        }
    

class SchoolDraftUpdateSubmissionNotification(EntrySubmissionNotification):

    def compose_notification(self):
        title = f"School Submission (Update): {self.data['name']}"
        detail = f"An update to your school entry: {self.data['name']} has been submitted successfully and is now under review.\nEntry:\n"
        for item, i in zip(self.data, range(len(self.data))):
            detail += f"{i+1}. {item}: {self.data[item]}\n"
        
        return {
            "type": Notification.SUBMISSION,
            "title": title,
            "detail": detail
        }


class SupervisorCountryDraftSubmissionNotification(EntrySubmissionNotification):

    def compose_notification(self):
        title = f"Supervisor Country Submission: {self.data['name']}"
        detail = f"Your country entry: {self.data['name']} has been submitted successfully and is awaiting publishing.\n\nEntry:\n"
        for item, i in zip(self.data, range(len(self.data))):
            detail += f"{i+1}. {item}: {self.data[item]}\n"
        
        return {
            "type": Notification.SUBMISSION,
            "title": title,
            "detail": detail
        }
    

class SupervisorCountryDraftUpdateSubmissionNotification(EntrySubmissionNotification):

    def compose_notification(self):
        title = f"Supervisor Country Submission (Update): {self.data['name']}"
        detail = f"An update to your country entry: {self.data['name']} has been submitted successfully and is awaiting publishing.\n\nEntry:\n"
        for item, i in zip(self.data, range(len(self.data))):
            detail += f"{i+1}. {item}: {self.data[item]}\n"
        
        return {
            "type": Notification.SUBMISSION,
            "title": title,
            "detail": detail
        }


class SupervisorCurrencyDraftSubmissionNotification(EntrySubmissionNotification):

    def compose_notification(self):
        title = f"Supervisor Currency Submission: {self.data['name']}"
        detail = f"Your currency entry: {self.data['name']} has been submitted successfully and is awaiting publishing.\n\nEntry:\n"
        for item, i in zip(self.data, range(len(self.data))):
            detail += f"{i+1}. {item}: {self.data[item]}\n"
        
        return {
            "type": Notification.SUBMISSION,
            "title": title,
            "detail": detail
        }
    

class SupervisorCurrencyDraftUpdateSubmissionNotification(EntrySubmissionNotification):

    def compose_notification(self):
        title = f"Supervisor Currency Submission (Update): {self.data['name']}"
        detail = f"An update to your currency entry: {self.data['name']} has been submitted successfully and is awaiting publishing.\n\nEntry:\n"
        for item, i in zip(self.data, range(len(self.data))):
            detail += f"{i+1}. {item}: {self.data[item]}\n"
        
        return {
            "type": Notification.SUBMISSION,
            "title": title,
            "detail": detail
        }


class SupervisorDegreeTypeSubmissionNotification(EntrySubmissionNotification):

    def compose_notification(self):
        title = f"Supervisor DegreeType Submission: {self.data['name']}"
        detail = f"Your degree type entry: {self.data['name']} has been submitted successfully and is awaiting publishing.\n\nEntry:\n"
        for item, i in zip(self.data, range(len(self.data))):
            detail += f"{i+1}. {item}: {self.data[item]}\n"
        
        return {
            "type": Notification.SUBMISSION,
            "title": title,
            "detail": detail
        }


class SupervisorDisciplineDraftSubmissionNotification(EntrySubmissionNotification):

    def compose_notification(self):
        title = f"Supervisor Discipline Submission: {self.data['name']}"
        detail = f"Your discipline entry: {self.data['name']} has been submitted successfully and is awaiting publishing.\n\nEntry:\n"
        for item, i in zip(self.data, range(len(self.data))):
            detail += f"{i+1}. {item}: {self.data[item]}\n"
        
        return {
            "type": Notification.SUBMISSION,
            "title": title,
            "detail": detail
        }
    

class SupervisorDisciplineDraftUpdateSubmissionNotification(EntrySubmissionNotification):

    def compose_notification(self):
        title = f"Supervisor Discipline Submission (Update): {self.data['name']}"
        detail = f"An update to your discipline entry: {self.data['name']} has been submitted successfully and is awaiting publishing.\n\nEntry:\n"
        for item, i in zip(self.data, range(len(self.data))):
            detail += f"{i+1}. {item}: {self.data[item]}\n"
        
        return {
            "type": Notification.SUBMISSION,
            "title": title,
            "detail": detail
        }


class SupervisorLanguageDraftSubmissionNotification(EntrySubmissionNotification):

    def compose_notification(self):
        title = f"Supervisor Language Submission: {self.data['name']}"
        detail = f"Your language entry: {self.data['name']} has been submitted successfully and is awaiting publishing.\n\nEntry:\n"
        for item, i in zip(self.data, range(len(self.data))):
            detail += f"{i+1}. {item}: {self.data[item]}\n"
        
        return {
            "type": Notification.SUBMISSION,
            "title": title,
            "detail": detail
        }


class SupervisorLanguageDraftUpdateSubmissionNotification(EntrySubmissionNotification):

    def compose_notification(self):
        title = f"Supervisor Language Submission (Update): {self.data['name']}"
        detail = f"An update to your language entry: {self.data['name']} has been submitted successfully and is awaiting publishing.\n\nEntry:\n"
        for item, i in zip(self.data, range(len(self.data))):
            detail += f"{i+1}. {item}: {self.data[item]}\n"
        
        return {
            "type": Notification.SUBMISSION,
            "title": title,
            "detail": detail
        }

