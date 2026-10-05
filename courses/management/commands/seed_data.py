from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from courses.models import Course, Lesson


User = get_user_model()


class Command(BaseCommand):
    help = "Create dummy authors, student, courses and lessons"


    def handle(self, *args, **options):

        self.stdout.write("Creating dummy data...\n")


        # =========================================================
        # AUTHORS
        # =========================================================

        authors_data = [
            {
                "username": "rahul_dev",
                "email": "rahul.dev@example.com",
                "password": "Rahul@123",
                "bio": "Rahul Sharma - Full Stack Developer",
            },
            {
                "username": "priya_python",
                "email": "priya.python@example.com",
                "password": "Priya@123",
                "bio": "Priya Patel - Python and Backend Developer",
            },
            {
                "username": "amit_cloud",
                "email": "amit.cloud@example.com",
                "password": "Amit@123",
                "bio": "Amit Shah - DevOps and Cloud Engineer",
            },
        ]


        authors = {}

        for data in authors_data:

            user, created = User.objects.get_or_create(
                username=data["username"],
                defaults={
                    "email": data["email"],
                    "bio": data["bio"],
                }
            )

            if created:
                user.set_password(data["password"])
                user.save()

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created author: {data['username']}"
                    )
                )
            else:
                self.stdout.write(
                    f"Author already exists: {data['username']}"
                )

            authors[data["username"]] = user


        # =========================================================
        # STUDENT
        # =========================================================

        student, created = User.objects.get_or_create(
            username="student01",
            defaults={
                "email": "student01@example.com",
                "bio": "Learning programming and web development.",
            }
        )

        if created:
            student.set_password("Student@123")
            student.save()

            self.stdout.write(
                self.style.SUCCESS(
                    "Created student: student01"
                )
            )
        else:
            self.stdout.write(
                "Student already exists: student01"
            )


        # =========================================================
        # COURSES
        # =========================================================

        courses_data = [

            {
                "title": "Complete React JS for Beginners",
                "description": (
                    "Learn React JS from the basics and build modern "
                    "interactive web applications using components, "
                    "props, state, hooks and API integration."
                ),
                "instructor": "rahul_dev",
                "price": 799,
                "category": "web",
                "status": "published",

                "lessons": [
                    (
                        "Introduction to React",
                        "Learn what React is, why it is used and how to create your first React project."
                    ),
                    (
                        "Components and JSX",
                        "Learn functional components, JSX syntax and reusable components."
                    ),
                    (
                        "Props and State",
                        "Understand props, state and how data flows between React components."
                    ),
                    (
                        "React Events and Forms",
                        "Learn event handling, form inputs and controlled components."
                    ),
                    (
                        "React Hooks",
                        "Learn useState, useEffect and the basics of React Hooks."
                    ),
                    (
                        "Fetching Data from APIs",
                        "Learn how to fetch API data and display loading and response states."
                    ),
                ],
            },


            {
                "title": "Python Django REST API",
                "description": (
                    "Build a complete REST API using Python, Django and "
                    "Django REST Framework with authentication, database "
                    "models and JWT security."
                ),
                "instructor": "priya_python",
                "price": 999,
                "category": "programming",
                "status": "published",

                "lessons": [
                    (
                        "Introduction to Django",
                        "Learn Django architecture, project structure and how to run a Django application."
                    ),
                    (
                        "Models and Database",
                        "Learn Django models, migrations and database relationships."
                    ),
                    (
                        "Django REST Framework",
                        "Learn serializers, API views, requests and responses."
                    ),
                    (
                        "Authentication with JWT",
                        "Learn login, access tokens and refresh tokens."
                    ),
                    (
                        "Permissions and Authorization",
                        "Learn IsAuthenticated and custom permissions for protected APIs."
                    ),
                    (
                        "Building a Complete REST API",
                        "Build CRUD APIs and understand REST API best practices."
                    ),
                ],
            },


            {
                "title": "Java Spring Boot Backend Development",
                "description": (
                    "Learn Spring Boot by building REST APIs with Java, "
                    "Spring Data JPA, MySQL and Spring Security."
                ),
                "instructor": "rahul_dev",
                "price": 1199,
                "category": "programming",
                "status": "published",

                "lessons": [
                    (
                        "Introduction to Spring Boot",
                        "Learn Spring Boot, project structure and how to create your first application."
                    ),
                    (
                        "REST APIs",
                        "Learn controllers and how to create GET, POST, PUT and DELETE APIs."
                    ),
                    (
                        "Spring Data JPA",
                        "Learn entities, repositories and database relationships."
                    ),
                    (
                        "MySQL Database",
                        "Connect Spring Boot with MySQL and perform database operations."
                    ),
                    (
                        "Spring Security",
                        "Learn authentication, authorization and securing REST endpoints."
                    ),
                    (
                        "JWT Authentication",
                        "Learn JWT structure, login APIs and protected endpoints."
                    ),
                ],
            },


            {
                "title": "Docker and DevOps Fundamentals",
                "description": (
                    "Learn the fundamentals of Docker and DevOps and "
                    "understand how to containerize and deploy modern "
                    "web applications."
                ),
                "instructor": "amit_cloud",
                "price": 899,
                "category": "devops",
                "status": "published",

                "lessons": [
                    (
                        "Introduction to DevOps",
                        "Learn what DevOps is and understand development, deployment and CI/CD."
                    ),
                    (
                        "Introduction to Docker",
                        "Learn containers, Docker images and Docker architecture."
                    ),
                    (
                        "Dockerfile",
                        "Learn how to create Dockerfiles, build images and run containers."
                    ),
                    (
                        "Docker Compose",
                        "Learn how to manage multiple containers and services."
                    ),
                    (
                        "Deploying Applications",
                        "Learn production builds, deployment and environment configuration."
                    ),
                    (
                        "CI/CD Basics",
                        "Learn GitHub workflows, automated builds and deployment pipelines."
                    ),
                ],
            },
        ]


        # =========================================================
        # CREATE COURSES + LESSONS
        # =========================================================

        for course_data in courses_data:

            instructor = authors[course_data["instructor"]]

            course, created = Course.objects.get_or_create(
                title=course_data["title"],
                instructor=instructor,
                defaults={
                    "description": course_data["description"],
                    "price": course_data["price"],
                    "category": course_data["category"],
                    "status": course_data["status"],
                }
            )


            if created:

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created course: {course.title}"
                    )
                )

            else:

                self.stdout.write(
                    f"Course already exists: {course.title}"
                )


            # =====================================================
            # LESSONS
            # =====================================================

            for index, lesson_data in enumerate(
                course_data["lessons"],
                start=1
            ):

                lesson, lesson_created = Lesson.objects.get_or_create(
                    course=course,
                    order=index,
                    defaults={
                        "title": lesson_data[0],
                        "content": lesson_data[1],
                    }
                )

                if lesson_created:

                    self.stdout.write(
                        f"   Created lesson {index}: {lesson.title}"
                    )

                else:

                    self.stdout.write(
                        f"   Lesson already exists: {lesson.title}"
                    )


        # =========================================================
        # FINAL MESSAGE
        # =========================================================

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                "========================================"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                "Dummy data created successfully!"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                "========================================"
            )
        )

        self.stdout.write("")

        self.stdout.write("Authors:")

        self.stdout.write(
            "  rahul_dev / Rahul@123"
        )

        self.stdout.write(
            "  priya_python / Priya@123"
        )

        self.stdout.write(
            "  amit_cloud / Amit@123"
        )

        self.stdout.write("")

        self.stdout.write("Student:")

        self.stdout.write(
            "  student01 / Student@123"
        )

        self.stdout.write("")

        self.stdout.write(
            "Created: 4 courses + 24 lessons"
        )