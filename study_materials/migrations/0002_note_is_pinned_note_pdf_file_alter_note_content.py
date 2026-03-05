
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
    ('study_materials', '0001_initial'),
    ]

    

    operations = [
        migrations.AddField(
            model_name='note',
            name='is_pinned',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='note',
            name='pdf_file',
            field=models.FileField(blank=True, null=True, upload_to='user_pdfs/'),
        ),
        migrations.AlterField(
            model_name='note',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
    ]
