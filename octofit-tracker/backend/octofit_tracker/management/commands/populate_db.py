from django.core.management.base import BaseCommand
from octofit_tracker.models import Team, User, Activity, Workout, Leaderboard
from django.db import transaction

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):

        with transaction.atomic():
            # Clear existing data in correct order to avoid FK issues and unhashable errors
            for obj in Leaderboard.objects.all():
                obj.delete()
            for obj in Activity.objects.all():
                obj.delete()
            for workout in Workout.objects.all():
                workout.suggested_for.clear()
                workout.delete()
            for obj in User.objects.all():
                obj.delete()
            for obj in Team.objects.all():
                obj.delete()

            # Create teams
            marvel = Team.objects.create(name='Marvel')
            dc = Team.objects.create(name='DC')

            # Create users
            users = [
                User.objects.create(name='Spider-Man', email='spiderman@marvel.com', team=marvel),
                User.objects.create(name='Iron Man', email='ironman@marvel.com', team=marvel),
                User.objects.create(name='Wonder Woman', email='wonderwoman@dc.com', team=dc),
                User.objects.create(name='Batman', email='batman@dc.com', team=dc),
            ]

            # Create activities
            Activity.objects.create(user=users[0], type='Running', duration=30, date='2026-01-01')
            Activity.objects.create(user=users[1], type='Cycling', duration=45, date='2026-01-02')
            Activity.objects.create(user=users[2], type='Swimming', duration=60, date='2026-01-03')
            Activity.objects.create(user=users[3], type='Yoga', duration=50, date='2026-01-04')

            # Create workouts
            workout1 = Workout.objects.create(name='Hero HIIT', description='High intensity interval training for heroes.')
            workout2 = Workout.objects.create(name='Power Yoga', description='Yoga for strength and flexibility.')
            workout1.suggested_for.set([users[0], users[1]])
            workout2.suggested_for.set([users[2], users[3]])

            # Create leaderboard
            Leaderboard.objects.create(team=marvel, points=100)
            Leaderboard.objects.create(team=dc, points=90)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
