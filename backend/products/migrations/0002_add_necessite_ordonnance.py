from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicament',
            name='necessite_ordonnance',
            field=models.BooleanField(default=False, verbose_name='Nécessite ordonnance'),
        ),
    ]
