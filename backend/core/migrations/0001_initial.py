
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    initial = True # Indicates this is the first migration for the app

    operations = [
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=500)),
                ('url', models.URLField(blank=True, max_length=2000, null=True)),
                ('domain', models.CharField(blank=True, max_length=255, null=True)),
                ('score', models.IntegerField(default=0)),
                ('comments_count', models.IntegerField(default=0)),
                ('author', models.CharField(max_length=255)),
                ('timestamp', models.DateTimeField()),
                ('fetched_at', models.DateTimeField(auto_now_add=True)), 
                ('updated_at', models.DateTimeField(auto_now=True)),   
                ('is_ai_related', models.BooleanField(default=False)), 
            ],
        ),
        migrations.CreateModel(
            name='DomainStats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')), 
                ('domain', models.CharField(max_length=255, unique=True)), 
                ('count', models.IntegerField(default=0)),
                ('last_updated', models.DateTimeField(auto_now=True)), 
            ],
        ),
        migrations.CreateModel(
            name='KeywordMention',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')), 
                ('keyword', models.CharField(max_length=100)),
                ('story', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='keywords', to='core.story')),
            ],
            options={
                'unique_together': {('keyword', 'story')},
            },
        ),
    ] 