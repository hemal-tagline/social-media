from django.db import models

# Create your models here.

class Program(models.Model):
    name = models.CharField(max_length=255)
    school = models.CharField(max_length=255)
    department = models.CharField(max_length=255)

    class Meta:
        verbose_name = ("Program")
        verbose_name_plural = ("Programs")
        db_table = "program"

    def __str__(self):
        return self.name


class ProgramOutcome(models.Model):
    description = models.CharField(max_length=255)
    program = models.ForeignKey(
        Program,related_name='outcomes', on_delete=models.CASCADE)

    class Meta:
        verbose_name = ("Program Outcome")
        verbose_name_plural = ("Program Outcomes")
        db_table = "program_outcome"

    def __str__(self):
        return self.description
    
class Course(models.Model):
    CREDIT_HOURS = (
        (0, '---Please select credit hour---'),
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
    )

    code = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    length = models.PositiveIntegerField(blank=True,default=0)
    credit_hours = models.PositiveIntegerField(
        choices=CREDIT_HOURS, blank=True, default=0)
    program = models.ForeignKey(
        Program, on_delete=models.CASCADE, null=True, blank=True)
    module_order = models.TextField(blank=True)
    
    class Meta:
        verbose_name = ("Course")
        verbose_name_plural = ("Courses")
        db_table = "course"

    def __str__(self):
        return self.code


class CourseOutcome(models.Model):
    description = models.CharField(max_length=255)
    plo_addressed = models.ManyToManyField(ProgramOutcome,related_name="plo_addressed", blank=True)
    course = models.ForeignKey(
        Course, related_name='outcomes', on_delete=models.CASCADE)

    class Meta:
        verbose_name = ("Course Outcome")
        verbose_name_plural = ("Course Outcomes")
        db_table = "course_outcome"

    def __str__(self):
        return self.description
    