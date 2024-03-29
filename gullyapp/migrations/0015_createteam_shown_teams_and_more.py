# Generated by Django 4.2.7 on 2023-12-17 02:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gullyapp', '0014_shownteamshistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='createteam',
            name='shown_teams',
            field=models.ManyToManyField(blank=True, related_name='teams_shown', to='gullyapp.shownteamshistory'),
        ),
        migrations.AlterField(
            model_name='shownteamshistory',
            name='shown_team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shown_teams_history', to='gullyapp.createteam'),
        ),
    ]
