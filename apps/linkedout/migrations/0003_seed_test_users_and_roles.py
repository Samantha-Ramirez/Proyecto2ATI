from django.db import migrations
from django.contrib.auth.hashers import make_password


def seed_users_and_roles(apps, schema_editor):
    User = apps.get_model("auth", "User")
    Group = apps.get_model("auth", "Group")
    Profile = apps.get_model("linkedout", "Profile")

    company_group, _ = Group.objects.get_or_create(name="Company")
    prof_group, _ = Group.objects.get_or_create(name="Professional")

    # Password común
    hashed_pw = make_password("loslinkedout")

    admin_user, created_admin = User.objects.get_or_create(
        username="admin",
        defaults={
            "email": "admin@example.com",
            "first_name": "Admin",
            "last_name": "System",
            "is_active": True,
            "is_staff": True,
            "is_superuser": True,
            "password": hashed_pw,
        },
    )
    if not created_admin and not admin_user.is_superuser:
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.save(update_fields=["is_staff", "is_superuser"])

    # --- 2. SEEDER PARA USUARIO COMPANY ---
    test_company, created_company = User.objects.get_or_create(
        username="test_company",
        defaults={
            "email": "test_company@example.com",
            "first_name": "Test",
            "last_name": "Company",
            "is_active": True,
            "password": hashed_pw,
        },
    )
    # Si ya existía pero no tiene password usable, se la fijamos igual
    if not created_company and (not test_company.password):
        test_company.password = hashed_pw
        test_company.save(update_fields=["password"])

    test_professional, created_prof = User.objects.get_or_create(
        username="test_professional",
        defaults={
            "email": "test_professional@example.com",
            "first_name": "Test",
            "last_name": "Professional",
            "is_active": True,
            "password": hashed_pw,
        },
    )
    if not created_prof and (not test_professional.password):
        test_professional.password = hashed_pw
        test_professional.save(update_fields=["password"])

    # Asignar grupos
    test_company.groups.add(company_group)
    test_professional.groups.add(prof_group)

    # Crear perfiles
    Profile.objects.get_or_create(
        user=test_company,
        defaults={"user_type": "company"},
    )
    Profile.objects.get_or_create(
        user=test_professional,
        defaults={"user_type": "professional"},
    )


def unseed_users_and_roles(apps, schema_editor):
    User = apps.get_model("auth", "User")
    Profile = apps.get_model("linkedout", "Profile")

    usernames = ["test_company", "test_professional", "admin"]

    Profile.objects.filter(user__username__in=usernames).delete()
    User.objects.filter(username__in=usernames).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("linkedout", "0002_profile"),
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.RunPython(seed_users_and_roles, unseed_users_and_roles),
    ]
