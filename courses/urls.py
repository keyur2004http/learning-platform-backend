from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LessonViewSet,ReviewViewSet

router = DefaultRouter()

router.register('courses', CourseViewSet)
router.register('lessons', LessonViewSet)
router.register('reviews', ReviewViewSet)

urlpatterns = router.urls
