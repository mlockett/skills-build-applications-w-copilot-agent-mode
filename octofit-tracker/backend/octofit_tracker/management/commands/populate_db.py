from django.core.management.base import BaseCommand
from octofit_tracker.models import Team, User, Activity, Workout, Leaderboard
from django.db import transaction

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        with transaction.atomic():
            # Clear existing data
            Leaderboard.objects.all().delete()
            Activity.objects.all().delete()
            Workout.objects.all().delete()
            User.objects.all().delete()
            Team.objects.all().delete()

            # Create teams
            marvel = Team.objects.create(name='Marvel')
            dc = Team.objects.create(name='DC')

            # Create users
            users = [
                User(name='Spider-Man', email='spiderman@marvel.com', team=marvel),
                User(name='Iron Man', email='ironman@marvel.com', team=marvel),
                User(name='Wonder Woman', email='wonderwoman@dc.com', team=dc),
                User(name='Batman', email='batman@dc.com', team=dc),
            ]
            for user in users:
                user.save()

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
