from rest_framework import serializers

from academics.models import Country, Course, Currency, DegreeType, Discipline, Language, ProgrammeType, School

from action.models import Action


# class EntryObjectRelatedField(serializers.RelatedField):

#     def to_representation(self, entry):
#         """
#         Serialize tagged objects to a simple textual representation.
#         """
#         if isinstance(entry, Country):
#             return 'Country: ' + entry.id
#         elif isinstance(entry, Course):
#             return 'Course: ' + entry.id
#         elif isinstance(entry, Currency):
#             return 'Currency: ' + entry.id
#         elif isinstance(entry, DegreeType):
#             return 'DegreeType: ' + entry.id
#         elif isinstance(entry, Discipline):
#             return 'Discipline: ' + entry.id
#         elif isinstance(entry, Language):
#             return 'Language: ' + entry.id
#         elif isinstance(entry, ProgrammeType):
#             return 'ProgrammeType: ' + entry.id
#         elif isinstance(entry, School):
#             return 'School: ' + entry.id
#         raise Exception('Unexpected type of entry object')


class CreateActionSerializer(serializers.ModelSerializer):

    # entry = EntryObjectRelatedField()

    class Meta:
        model = Action
        fields = (
            "id",
            "title",
            "detail",
            "entry_object_type",
            "entry_object_id"
        )


class ListActionSerializer(serializers.ModelSerializer):

    ...


class DetailActionSerializer(serializers.ModelSerializer):
    
    ...


class UpdateActionSerializer(serializers.ModelSerializer):

    ...


class DeleteActionSerializer(serializers.ModelSerializer):

    ...