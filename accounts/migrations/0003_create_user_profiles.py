from django.db import migrations

def create_profiles(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    UserProfile = apps.get_model('accounts', 'UserProfile')
    
    for user in User.objects.all():
        UserProfile.objects.get_or_create(user=user)

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', "0002_alter_userprofile_mobile_number"),  # Replace with your previous migration
    ]

    operations = [
        migrations.RunPython(create_profiles),
    ]