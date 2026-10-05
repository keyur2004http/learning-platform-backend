from rest_framework import serializers
from .models import Course, Lesson, Enrollment,Review


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            'id',
            'title',
            'description',
            'instructor',
            'category',
            'status',
            'price',
            'created_at'
        ]
        read_only_fields = ['id', 'instructor', 'created_at']

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = [
            'id',
            'course',
            'title',
            'content',
            'order',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = [
            'id',
            'student',
            'course',
            'enrolled_at'
        ]
        read_only_fields = ['id', 'student', 'enrolled_at']        

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            'id',
            'student',
            'course',
            'rating',
            'comment',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'id',
            'student',
            'course',
            'created_at',
            'updated_at'
        ]

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError(
                'Rating must be between 1 and 5.'
            )
        return value