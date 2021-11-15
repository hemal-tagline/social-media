from .models import *
from rest_framework import serializers


class ProgramOutcomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramOutcome
        fields = ('id', 'description')
        extra_kwargs = {
            'program': {'required': False}
        }

    def create(self, validated_data):
        programoutcome = ProgramOutcome.objects.create(**validated_data, program_id=self.initial_data['program_id'])
        return programoutcome


class ProgramSerializer(serializers.ModelSerializer):
    outcomes = ProgramOutcomeSerializer(many=True )

    class Meta:
        model = Program
        fields = ('id', 'name', 'school', 'department', 'outcomes')
        
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['name'] = ret['name'].upper()
        return ret

    def create(self, validated_data):
        outcomes_data = validated_data.pop('outcomes')
        program = Program.objects.create(**validated_data)
        for outcome_data in outcomes_data:
            ProgramOutcome.objects.create(program=program, **outcome_data)
        return program

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.school = validated_data.get('school', instance.school)
        instance.department = validated_data.get(
            'department', instance.department)
        instance.save()
        return instance




class CourseOutcomeSerializer(serializers.ModelSerializer):
    plo_addressed = ProgramOutcomeSerializer(many=True, read_only=True)

    class Meta:
        model = CourseOutcome
        fields = ('id', 'description', 'plo_addressed')
        extra_kwargs = {
            'course': {'required': False}
        }


class ProgramSerializerReadOnly(serializers.ModelSerializer):

    class Meta:
        model = Program
        fields = ('id', 'name', 'school', 'department')


class CourseSerializer(serializers.ModelSerializer):
    outcomes = CourseOutcomeSerializer(many=True, required=False)

    class Meta:
        model = Course
        fields = ('id', 'code', 'title', 'description', 'length',
                  'credit_hours', 'program', 'outcomes')
        extra_kwargs = {
            'description': {'required': False},
            'length': {'required': False},
            'credit_hours': {'required': False},
            'program': {'required': False},
            'outcomes': {'required': False}
        }

    def create_outcomes(self, course):
        for outcome_data in self.initial_data['outcomes']:
            out = CourseOutcome.objects.create(course=course, description=outcome_data['description'])
            if 'program' in self.initial_data and 'plo_addressed' in outcome_data:
                for data in outcome_data["plo_addressed"]:
                    out.plo_addressed.add(data)
                    out.save()

    def create(self, validated_data):
        if 'outcomes' in validated_data:
            outcomes_data = validated_data.pop('outcomes')
            course = Course.objects.create(**validated_data)
            self.create_outcomes(course)
        else:
            course = Course.objects.create(**validated_data)
        return course

    def update(self, instance, validated_data):
        if 'outcomes' in validated_data:
            outcomes_data = validated_data.pop('outcomes')
        instance.code = validated_data.get('code', instance.code)
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.length = validated_data.get('length', instance.length)
        instance.credit_hours = validated_data.get(
            'credit_hours', instance.credit_hours)
        instance.program = validated_data.get('program', instance.program)

        instance.save()
        return instance


class CourseResponseSerializer(CourseSerializer):
    program = ProgramSerializerReadOnly(read_only=True)
