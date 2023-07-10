from django.test import TestCase
from django.contrib.auth.models import User
from .models import Instructor, Learner, Course, Lesson, Enrollment, Question, Choice, Submission

class OnlineCourseTestCase(TestCase):
    def setUp(self):
        # Create test users
        self.instructor = User.objects.create_user(username='instructor', password='testpass')
        self.learner = User.objects.create_user(username='learner', password='testpass')
        
        # Create instructor and learner profiles
        Instructor.objects.create(user=self.instructor, full_time=True, total_learners=100)
        Learner.objects.create(user=self.learner, occupation=Learner.STUDENT, social_link='https://example.com')
        
        # Create a course
        self.course = Course.objects.create(name='Test Course', description='This is a test course')
        
        # Add instructor to the course
        self.course.instructors.add(self.instructor)
        
        # Create a lesson
        self.lesson = Lesson.objects.create(title='Test Lesson', order=1, course=self.course, content='This is a test lesson')
        
        # Create questions and choices
        self.question1 = Question.objects.create(lesson=self.lesson, question_text='Question 1', grade=1.0)
        self.choice1 = Choice.objects.create(question=self.question1, choice_text='Choice 1', is_correct=True)
        self.choice2 = Choice.objects.create(question=self.question1, choice_text='Choice 2', is_correct=False)
        
        self.question2 = Question.objects.create(lesson=self.lesson, question_text='Question 2', grade=1.0)
        self.choice3 = Choice.objects.create(question=self.question2, choice_text='Choice 3', is_correct=True)
        self.choice4 = Choice.objects.create(question=self.question2, choice_text='Choice 4', is_correct=False)
        
    def test_enrollment(self):
        # Enroll the learner in the course
        enrollment = Enrollment.objects.create(user=self.learner, course=self.course, mode=Enrollment.HONOR)
        
        # Check if the learner is enrolled in the course
        self.assertEqual(enrollment.user, self.learner)
        self.assertEqual(enrollment.course, self.course)
        
        # Check if the course has the correct total enrollment count
        self.assertEqual(self.course.total_enrollment, 1)
        
    def test_submission(self):
        # Enroll the learner in the course
        enrollment = Enrollment.objects.create(user=self.learner, course=self.course, mode=Enrollment.HONOR)
        
        # Create a submission
        submission = Submission.objects.create(enrollment=enrollment)
        
        # Add choices to the submission
        submission.choices.add(self.choice1, self.choice3)
        
        # Check if the submission is associated with the correct enrollment
        self.assertEqual(submission.enrollment, enrollment)
        
        # Check if the submission has the correct choices
        self.assertIn(self.choice1, submission.choices.all())
        self.assertIn(self.choice3, submission.choices.all())

