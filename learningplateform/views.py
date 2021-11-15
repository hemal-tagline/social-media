from .models import *
from .serializer import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404


class ProgramListView(APIView):
    def get(self, request, pk=None):
        programs = Program.objects.all()
        program_serializer = ProgramSerializer(programs, many=True)
        return Response(program_serializer.data)
    
    def post(self, request, format=None):
        program_serializer = ProgramSerializer(data=request.data)
        if program_serializer.is_valid():
            program_serializer.save()
            return Response(program_serializer.data, status=status.HTTP_201_CREATED)
        return Response(program_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProgramDeatilView(APIView):

    def get_object(self, pk):
        try:
            return Program.objects.get(pk=pk)
        except Program.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        obj = self.get_object(pk)
        program_serializer = ProgramSerializer(obj)
        return Response(program_serializer.data)

    def delete(self, request, pk, format=None):
        obj = self.get_object(pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def serializer_valid_save(self,serializer, response_data):
        if serializer.is_valid():
            serializer.save()
            response_data.append(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return response_data
    
    def put(self, request, pk, format=None):
        response_data = []
        outcomes_id = []
        program = self.get_object(pk)
        serializer = ProgramSerializer(instance=program, data=request.data)
        if serializer.is_valid():
            serializer.save()
            program_response = serializer.data
            
            for obj in request.data['outcomes']:
                if 'id' in obj:
                    try:
                        program_instance = ProgramOutcome.objects.get(pk=obj['id'], program=program_response['id'])
                    except:
                        return Response({"id": f'Invalid pk \"{obj["id"]}\" object does not exist.'}, status=status.HTTP_404_NOT_FOUND)
                    serializer = ProgramOutcomeSerializer(instance=program_instance, data=obj)
                    response_data = self.serializer_valid_save(serializer, response_data)
                else:
                    obj['program_id'] = program_response['id']
                    serializer = ProgramOutcomeSerializer(data=obj)
                    response_data = self.serializer_valid_save(serializer, response_data)
                    
                outcomes_id.append(serializer.data['id'])
            results = ProgramOutcome.objects.filter(program=program_response['id'])
            for result in results:
                if result.id not in outcomes_id:
                    ProgramOutcome.objects.filter(pk=result.id).delete()
            program_response['outcomes'] = response_data
            return Response(program_response, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseListView(APIView):

    def get(self, request, pk=None):
        course = Course.objects.all()
        course_serializer = CourseSerializer(course, many=True,context={'request': request})
        return Response(course_serializer.data)

    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if 'program' in request.data and 'outcomes' in request.data:
            for outcome in request.data['outcomes']:
                if 'plo_addressed' in outcome:
                    for plo_addressed_id in outcome['plo_addressed']:
                        try:
                            ProgramOutcome.objects.get(
                                pk=plo_addressed_id, program=request.data['program'])
                        except:
                            return Response({"plo_addressed": f'Invalid pk \"{plo_addressed_id}\" object does not exist in ProgramOutcome'}, status=status.HTTP_404_NOT_FOUND)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseDeatilView(APIView):
    def get_object(self, id):
        try:
            return Course.objects.get(id=id)
        except Course.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        getObj = self.get_object(pk)
        serializer = CourseResponseSerializer(getObj)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        course_respone = None
        outcome_respone = []
        outcome_id = []

        if 'program' in request.data and 'outcomes' in request.data:
            for outcome in request.data['outcomes']:
                if 'plo_addressed' in outcome:
                    for plo_addressed_id in outcome['plo_addressed']:
                        try:
                            ProgramOutcome.objects.get(
                                pk=plo_addressed_id, program=request.data['program'])
                        except:
                            return Response({"plo_addressed": f'Invalid pk \"{plo_addressed_id}\" object does not exist in ProgramOutcome'}, status=status.HTTP_404_NOT_FOUND)
        getObj = self.get_object(pk)
        serializer = CourseSerializer(getObj, data=request.data)

        if serializer.is_valid():
            serializer.save()
            if 'program' in request.data:
                getData = Course.objects.get(pk=getObj.id)
                getData.program_id = request.data['program']
                getData.save()

            else:
                getData = Course.objects.get(pk=getObj.id)
                getData.program_id = None
                getData.save()

            serializer = CourseSerializer(getData,data=request.data)
            if serializer.is_valid():
                serializer.save()

            course_respone = serializer.data
            if 'outcomes' in request.data:
                for outCome in request.data['outcomes']:
                    if 'id' in outCome:
                        try:
                            course_instance = CourseOutcome.objects.get(
                                id=outCome['id'], course=pk)
                            course_instance.plo_addressed.set(
                                outCome['plo_addressed'])
                        except:
                            return Response({"id": f'Invalid pk \"{outCome["id"]}\" object does not exist.'}, status=status.HTTP_404_NOT_FOUND)
                        serializer = CourseOutcomeSerializer(
                            instance=course_instance, data=outCome)
                        if serializer.is_valid():
                            serializer.save()
                            outcome_respone.append(serializer.data)
                    else:
                        courseoutcome = CourseOutcome.objects.create(
                            description=outCome['description'], course=getObj)
                        if 'plo_addressed' in outCome:
                            courseoutcome.plo_addressed.set(
                                outCome['plo_addressed'])

                        serializer = CourseOutcomeSerializer(courseoutcome)
                        outcome_respone.append(serializer.data)
                    outcome_id.append(serializer.data['id'])

            results = CourseOutcome.objects.filter(course=pk)
            for result in results:
                if result.id not in outcome_id:
                    data = CourseOutcome.objects.filter(pk=result.id).delete()
            course_respone['outcomes'] = outcome_respone
            return Response(course_respone, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        getObj = self.get_object(pk)
        getObj.delete()
        return Response({"messages": "record deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
