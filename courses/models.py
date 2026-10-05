from django.db import models
from users.models import User


class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    instructor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='courses'
    )
    CATEGORY_CHOICES = [
        ('programming', 'Programming'),
        ('web', 'Web Development'),
        ('database', 'Database'),
        ('devops', 'DevOps'),
        ('other', 'Other'),
    ]
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='other'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )

    created_at = models.DateTimeField(auto_now_add=True)
class Lesson(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons'
    )
    title = models.CharField(max_length=200)
    content = models.TextField()
    order = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Enrollment(models.Model):
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'course'],
                name='unique_student_course'
            )
        ]

    def __str__(self):
        return f'{self.student.username} - {self.course.title}'

class LessonProgress(models.Model):
    enrollment = models.ForeignKey(
        Enrollment,
        on_delete=models.CASCADE,
        related_name='progress'
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='progress'
    )
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['enrollment', 'lesson'],
                name='unique_enrollment_lesson'
            )
        ]

    def __str__(self):
        return f'{self.enrollment.student.username} - {self.lesson.title}'

class Review(models.Model):
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    rating = models.PositiveIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'course'],
                name='unique_student_course_review'
            )
        ]

    def __str__(self):
        return f'{self.student.username} - {self.course.title}'