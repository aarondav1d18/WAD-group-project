# Generated by Django 2.2 on 2025-03-28 04:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('is_fun', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('name', models.CharField(max_length=64)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('views', models.IntegerField(default=0)),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('image', models.CharField(default='/static/images/default_quiz.jpg', max_length=255)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='quizzes', to='app.Category')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('saved_quizes', models.ManyToManyField(blank=True, related_name='saved_by_users', to='app.Quiz')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StarRating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stars', models.IntegerField(choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='app.UserProfile')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='app.Quiz')),
            ],
        ),
        migrations.CreateModel(
            name='Slide',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=256)),
                ('image', models.ImageField(blank=True, null=True, upload_to='media/')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='slides', to='app.Quiz')),
            ],
        ),
        migrations.AddField(
            model_name='quiz',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quizzes', to='app.UserProfile'),
        ),
        migrations.AddField(
            model_name='category',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='app.UserProfile'),
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=64)),
                ('is_correct', models.BooleanField(default=False)),
                ('slide', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='app.Slide')),
            ],
        ),
    ]
