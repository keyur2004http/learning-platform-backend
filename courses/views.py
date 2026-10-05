from rest_framework import viewsets
from rest_framework.decorators import action
from .models import Course, Lesson,Enrollment, LessonProgress,Review
from .serializers import CourseSerializer, LessonSerializer, EnrollmentSerializer, ReviewSerializer
from .permissions import IsCourseInstructorOrReadOnly,IsLessonCourseInstructorOrReadOnly
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db.models import Avg, Count,Q

# Course Viewset
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsCourseInstructorOrReadOnly]

    def get_queryset(self):
        queryset = Course.objects.all()

        if not self.request.user.is_authenticated:
            queryset = queryset.filter(status='published')
        else:
            queryset = queryset.filter(
                Q(status='published') |
                Q(instructor=self.request.user)
            )

        search = self.request.query_params.get('search')
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        category = self.request.query_params.get('category')
        status = self.request.query_params.get('status')

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search)
            )

        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        if category:
            queryset = queryset.filter(category=category)

        if status:
            queryset = queryset.filter(status=status)

        return queryset

    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)
    @action(
        detail=True,
        methods=['GET'],
        url_path='lessons')
    def lessons(self, request, pk=None):
        course = self.get_object()
        lessons = course.lessons.all()
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data)
    @action(
    detail=True,
    methods=['POST'],
    url_path='enroll',
    permission_classes=[IsAuthenticated]
)
    def enroll(self, request, pk=None):
        course = self.get_object()
    
        if course.instructor == request.user:
            return Response(
                {'detail': 'You cannot enroll in your own course.'},
                status=400
            )
    
        if course.status != 'published':
            return Response(
                {'detail': 'You cannot enroll in a draft course.'},
                status=400
            )
    
        if Enrollment.objects.filter(
            student=request.user,
            course=course
        ).exists():
            return Response(
                {'detail': 'You are already enrolled in this course.'},
                status=400
            )
    
        enrollment = Enrollment.objects.create(
            student=request.user,
            course=course
        )
    
        serializer = EnrollmentSerializer(enrollment)
    
        return Response(
            serializer.data,
            status=201
        )
    @action(
      detail=False,
      methods=['GET'],
      url_path='my-courses',
      permission_classes=[IsAuthenticated]
    )
    def my_courses(self, request):
        courses = Course.objects.filter(
            enrollments__student=request.user
        )

        serializer = CourseSerializer(courses, many=True)

        return Response(serializer.data)
    @action(
    detail=False,
    methods=['GET'],
    url_path='my-progress',
    permission_classes=[IsAuthenticated]
)
    def my_progress(self, request):
        enrollments = Enrollment.objects.filter(
            student=request.user
        ).select_related('course')
    
        result = []
    
        for enrollment in enrollments:
            lessons = Lesson.objects.filter(
                course=enrollment.course
            )
    
            total_lessons = lessons.count()
    
            completed_lessons = LessonProgress.objects.filter(
                enrollment=enrollment,
                completed=True
            ).count()
    
            progress = 0
    
            if total_lessons > 0:
                progress = round(
                    (completed_lessons / total_lessons) * 100
                )
    
            result.append({
                'course_id': enrollment.course.id,
                'course_title': enrollment.course.title,
                'total_lessons': total_lessons,
                'completed_lessons': completed_lessons,
                'progress': progress
            })
    
        return Response(result)
    @action(
    detail=True,
    methods=['GET'],
    url_path='reviews'
)
    def reviews(self, request, pk=None):
        course = self.get_object()

        reviews = course.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)

        return Response(serializer.data)
    @action(
    detail=True,
    methods=['GET'],
    url_path='rating'
)
    def rating(self, request, pk=None):
        course = self.get_object()
    
        data = course.reviews.aggregate(
            average_rating=Avg('rating'),
            total_reviews=Count('id')
        )
    
        return Response({
            'course_id': course.id,
            'average_rating': data['average_rating'],
            'total_reviews': data['total_reviews']
        })
    @action(
    detail=False,
    methods=['GET'],
    url_path='my-created-courses',
    permission_classes=[IsAuthenticated]
)
    def my_created_courses(self, request):
        courses = Course.objects.filter(
            instructor=request.user
        )
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)
    @action(
    detail=True,
    methods=['GET'],
    url_path='progress',
    permission_classes=[IsAuthenticated]
)
    def progress(self, request, pk=None):
        course = self.get_object()

        enrollment = Enrollment.objects.filter(
            student=request.user,
            course=course
        ).first()

        if not enrollment:
            return Response(
                {
                    'detail': 'You are not enrolled in this course.'
                },
                status=403
            )

        lessons = course.lessons.all().order_by('order')

        result = []

        for lesson in lessons:
            progress = LessonProgress.objects.filter(
                enrollment=enrollment,
                lesson=lesson
            ).first()

            result.append({
                'lesson_id': lesson.id,
                'lesson_title': lesson.title,
                'order': lesson.order,
                'completed': progress.completed if progress else False,
                'completed_at': (
                    progress.completed_at
                    if progress else None
                )
            })

        total_lessons = len(result)
        completed_lessons = sum(
            1 for lesson in result
            if lesson['completed']
        )

        percentage = 0

        if total_lessons > 0:
            percentage = round(
                (completed_lessons / total_lessons) * 100
            )

        return Response({
            'course_id': course.id,
            'course_title': course.title,
            'total_lessons': total_lessons,
            'completed_lessons': completed_lessons,
            'progress': percentage,
            'lessons': result
        })
    @action(
    detail=False,
    methods=['GET'],
    url_path='dashboard',
    permission_classes=[IsAuthenticated]
)
    def dashboard(self, request):
        user = request.user
    
        # Student statistics
        enrollments = Enrollment.objects.filter(
            student=user
        ).select_related('course')
    
        total_enrolled_courses = enrollments.count()
    
        total_completed_lessons = LessonProgress.objects.filter(
            enrollment__student=user,
            completed=True
        ).count()
    
        total_lessons = Lesson.objects.filter(
            course__enrollments__student=user
        ).distinct().count()
    
        overall_progress = 0
    
        if total_lessons > 0:
            overall_progress = round(
                (total_completed_lessons / total_lessons) * 100
            )
    
        completed_courses = 0
    
        for enrollment in enrollments:
            course_lessons = Lesson.objects.filter(
                course=enrollment.course
            ).count()
    
            completed_lessons = LessonProgress.objects.filter(
                enrollment=enrollment,
                completed=True
            ).count()
    
            if course_lessons > 0 and completed_lessons == course_lessons:
                completed_courses += 1
    
        # Author statistics
        created_courses = Course.objects.filter(
            instructor=user
        )
    
        total_created_courses = created_courses.count()
    
        total_students = Enrollment.objects.filter(
            course__instructor=user
        ).values('student').distinct().count()
    
        return Response({
            'student': {
                'enrolled_courses': total_enrolled_courses,
                'completed_lessons': total_completed_lessons,
                'overall_progress': overall_progress,
                'completed_courses': completed_courses
            },
            'author': {
                'total_courses': total_created_courses,
                'total_students': total_students
            }
        })
class LessonViewSet(viewsets.ModelViewSet):

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.action == 'complete':
            return [IsAuthenticated()]

        return [IsLessonCourseInstructorOrReadOnly()]
    @action(
    detail=True,
    methods=['POST'],
    url_path='complete'
)
    def complete(self, request, pk=None):
        lesson = self.get_object()

        enrollment = Enrollment.objects.filter(
            student=request.user,
            course=lesson.course
        ).first()

        if not enrollment:
            return Response(
                {
                    'detail': 'You must be enrolled in this course.'
                },
                status=403
            )

        progress, created = LessonProgress.objects.get_or_create(
            enrollment=enrollment,
            lesson=lesson
        )

        if progress.completed:
            return Response({
                'message': 'Lesson is already completed.',
                'lesson_id': lesson.id,
                'completed': True,
                'completed_at': progress.completed_at
            })

        progress.completed = True
        progress.completed_at = timezone.now()
        progress.save()

        return Response({
            'message': 'Lesson completed successfully.',
            'lesson_id': lesson.id,
            'completed': True,
            'completed_at': progress.completed_at
        })

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
     course_id = self.request.data.get('course')

     enrollment = Enrollment.objects.filter(
         student=self.request.user,
         course_id=course_id
     ).first()

     if not enrollment:
         from rest_framework.exceptions import PermissionDenied
         raise PermissionDenied(
             'You must be enrolled in this course to review it.'
         )

     if Review.objects.filter(
         student=self.request.user,
         course_id=course_id
     ).exists():
         from rest_framework.exceptions import ValidationError
         raise ValidationError(
             {'detail': 'You have already reviewed this course.'}
         )

     serializer.save(
         student=self.request.user,
         course_id=course_id
     )
    def perform_update(self, serializer):
        if serializer.instance.student != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied(
                'You can only update your own review.'
            )

        serializer.save()

    def perform_destroy(self, instance):
        if instance.student != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied(
                'You can only delete your own review.'
            )

        instance.delete()