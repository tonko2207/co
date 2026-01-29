from django.db import migrations

ROLE_NAMES = [
    "Administrator systemu",
    "Pracownik schroniska",
    "Weterynarz",
    "Wolontariusz",
    "Kierownik schroniska",
    "Kierownik finansowy",
]

def add_perms(group, perms, Permission):
    """
    perms: lista krotek (app_label, codename), np. ('animals', 'add_animal')
    """
    for app_label, codename in perms:
        perm = Permission.objects.get(content_type__app_label=app_label, codename=codename)
        group.permissions.add(perm)

def create_roles(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")

    groups = {}
    for name in ROLE_NAMES:
        groups[name], _ = Group.objects.get_or_create(name=name)

    # --- PERMISSIONS ---

    # Administrator systemu: pe³ne permissions aplikacji animals
    # (prosto: bierzemy wszystkie perms z app_label='animals')
    admin_group = groups["Administrator systemu"]
    all_animals_perms = Permission.objects.filter(content_type__app_label="animals")
    admin_group.permissions.set(all_animals_perms)

    # Pracownik schroniska
    employee = groups["Pracownik schroniska"]
    add_perms(employee, [
        ("animals", "view_animal"),
        ("animals", "add_animal"),
        ("animals", "change_animal"),

        ("animals", "view_medicaldocument"),
        ("animals", "add_medicaldocument"),

        ("animals", "view_medicalvisit"),
        # ("animals", "add_medicalvisit"),  # odkomentuj jeœli pracownik ma dodawaæ wizyty
    ], Permission)

    # Weterynarz
    vet = groups["Weterynarz"]
    add_perms(vet, [
        ("animals", "view_animal"),

        ("animals", "view_medicalvisit"),
        ("animals", "add_medicalvisit"),
        ("animals", "change_medicalvisit"),

        ("animals", "view_medicaldocument"),
        ("animals", "add_medicaldocument"),
        ("animals", "change_medicaldocument"),
    ], Permission)

    # Wolontariusz
    volunteer = groups["Wolontariusz"]
    add_perms(volunteer, [
        ("animals", "view_animal"),
    ], Permission)

    # Kierownik schroniska
    manager = groups["Kierownik schroniska"]
    add_perms(manager, [
        ("animals", "view_animal"),
        ("animals", "change_animal"),

        ("animals", "view_medicalvisit"),
        ("animals", "view_medicaldocument"),
    ], Permission)

    # Kierownik finansowy (wgl¹d w koszty wizyt)
    finance = groups["Kierownik finansowy"]
    add_perms(finance, [
        ("animals", "view_medicalvisit"),
        # opcjonalnie:
        ("animals", "view_animal"),
    ], Permission)


def remove_roles(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Group.objects.filter(name__in=ROLE_NAMES).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("animals", "0006_medicaldocument"),
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.RunPython(create_roles, reverse_code=remove_roles),
    ]
