from django.core.management.base import BaseCommand
from faker import Faker
from kin.models import Category, Note, Priority, SubTask, Task

class Command(BaseCommand):
    help = 'Create initial data for task management application'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Clear existing data (optional — only for dev/testing)
        # self.clear_data()

        self.create_categories(5)
        self.create_priorities()
        self.create_tasks(20)
        self.create_subtasks(50)
        self.create_notes(30)

        self.stdout.write(self.style.SUCCESS('Initial task data created successfully.'))

    def create_categories(self, count):
        fake = Faker()
        for i in range(count):
            name = fake.word().title()
            Category.objects.get_or_create(name=name)
        self.stdout.write(self.style.SUCCESS(f'{count} categories created.'))

    def create_priorities(self):
        priorities = [
            {'level': 'Low', 'color': '#4CAF50'},
            {'level': 'Medium', 'color': '#FFC107'},
            {'level': 'High', 'color': '#F44336'},
        ]
        for p in priorities:
            Priority.objects.get_or_create(level=p['level'], defaults={'color': p['color']})
        self.stdout.write(self.style.SUCCESS('3 priorities created (Low, Medium, High).'))

    def create_tasks(self, count):
        fake = Faker()
        categories = list(Category.objects.all())
        priorities = list(Priority.objects.all())

        if not categories or not priorities:
            self.stdout.write(self.style.ERROR('No categories or priorities found. Create them first.'))
            return

        for _ in range(count):
            title = fake.sentence(nb_words=4).rstrip('.')
            description = fake.paragraph(nb_sentences=2)
            due_date = fake.date_between(start_date="today", end_date="+30d")
            completed = fake.boolean(chance_of_getting_true=30)
            category = fake.random_element(categories)
            priority = fake.random_element(priorities)

            Task.objects.create(
                title=title,
                description=description,
                due_date=due_date,
                completed=completed,
                category=category,
                priority=priority
            )
        self.stdout.write(self.style.SUCCESS(f'{count} tasks created.'))

    def create_subtasks(self, count):
        fake = Faker()
        tasks = list(Task.objects.all())

        if not tasks:
            self.stdout.write(self.style.ERROR('No tasks found. Create tasks first.'))
            return

        for _ in range(count):
            description = fake.sentence(nb_words=5).rstrip('.')
            completed = fake.boolean(chance_of_getting_true=50)
            task = fake.random_element(tasks)

            SubTask.objects.create(
                description=description,
                completed=completed,
                task=task
            )
        self.stdout.write(self.style.SUCCESS(f'{count} subtasks created.'))

    def create_notes(self, count):
        fake = Faker()
        tasks = list(Task.objects.all())

        if not tasks:
            self.stdout.write(self.style.ERROR('No tasks found. Create tasks first.'))
            return

        for _ in range(count):
            content = fake.paragraph(nb_sentences=3)
            task = fake.random_element(tasks)

            Note.objects.create(
                content=content,
                task=task
            )
        self.stdout.write(self.style.SUCCESS(f'{count} notes created.'))