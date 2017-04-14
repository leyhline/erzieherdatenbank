import os

from django.db import models
from django.core.validators import MaxValueValidator, RegexValidator

from .templatetags.activity_extras import RE_HASHTAG


def file_upload_path(instance, filename):
    last_file = instance.__class__.objects.order_by("-id").first()
    file_id = 1 if last_file is None else last_file.id + 1
    ext = os.path.splitext(filename)[1]
    classname = instance.__class__.__name__.lower()
    return "activity{}/{}{}{}".format(instance.activity_id, classname, file_id, ext)


class FieldOfEducation(models.Model):
    name = models.CharField(max_length=50, unique=True,
                            help_text="Maximal 50 Zeichen.",
                            verbose_name="Bildungsbereich")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Bildungsbereich"
        verbose_name_plural = "Bildungsbereiche"


class Material(models.Model):
    name = models.CharField(max_length=250, unique=True,
                            help_text="Maximal 250 Zeichen. Mehrzahl verwenden.",
                            verbose_name="Material")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Materialien"


class Season(models.Model):
    SPRING = 'F'
    SUMMER = 'S'
    AUTUMN = 'H'
    WINTER = 'W'
    SEASON_CHOICES = (
        (SPRING, "Frühling"),
        (SUMMER, "Sommer"),
        (AUTUMN, "Herbst"),
        (WINTER, "Winter"))
    name = models.CharField(max_length=1, choices=SEASON_CHOICES, primary_key=True,
                            verbose_name="Kürzel Jahreszeit")
    full_name = models.CharField(max_length=8, unique=True,
                                 verbose_name="Jahreszeit")

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Jahreszeit"
        verbose_name_plural = "Jahreszeiten"


class Tag(models.Model):
    # Match if there is a non-letter at the beginning or end of the word.
    tag_validator = RegexValidator(r"""\W+|\w+\W+""", inverse_match=True)
    name = models.CharField(max_length=50, unique=True, editable=False,
                            validators=[tag_validator],
                            help_text="Maximal 50 Zeichen.")

    def __str__(self):
        return self.name


class Activity(models.Model):
    ACTIVITY_CHOICES = (
        (None, "Egal"),
        (True, "Drinnen"),
        (False, "Draußen"))
    maximum_default = 99
    max_validator = MaxValueValidator(maximum_default)

    title = models.CharField(max_length=250, unique=True,
                             help_text="Maximal 250 Zeichen.",
                             verbose_name="Titel")
    min_age = models.PositiveSmallIntegerField(
                default=0, validators=[max_validator],
                help_text="Alter muss zwischen 0 und 99 liegen.",
                verbose_name="Mindestalter")
    max_age = models.PositiveSmallIntegerField(
                default=maximum_default, validators=[max_validator],
                help_text="Alter muss zwischen 0 und 99 liegen.",
                verbose_name="Maximalalter")
    groupsize_min = models.PositiveSmallIntegerField(
                default=0, validators=[max_validator],
                help_text="Gruppengröße muss zwischen 0 und 99 liegen.",
                verbose_name="minimale Gruppengröße")
    groupsize_max = models.PositiveSmallIntegerField(
                default=maximum_default, validators=[max_validator],
                help_text="Gruppengröße muss zwischen 0 und 99 liegen.",
                verbose_name="maximale Gruppengröße")
    source = models.CharField(max_length=2000, blank=True,
                              help_text="z.B. URL einer Website, Titel und Seites eines Buchs…",
                              verbose_name="Quelle")
    description = models.TextField(help_text="Ausführliche Angebotsbeschreibung.",
                                   verbose_name="Durchführung")
    setting = models.NullBooleanField(choices=ACTIVITY_CHOICES, default=None,
                                help_text=("Die Standardeinstellung ist für Angebote, "
                                           "die sowohl drinnen als auch draußen durchführbar sind."),
                                verbose_name="Umgebung")
    seasons = models.ManyToManyField(Season,
                                     help_text=("Zu welchen Jahreszeiten passt das Angebot? "
                                                "Ist die Jahreszeit egal, bitte alle auswählen."),
                                     verbose_name="Jahreszeiten")
    tags = models.ManyToManyField(Tag, blank=True,
                                  help_text=("Für beliebige Stichworte mit je Maximallänge 50. "
                                             "Tags werden direkt in der Beschreibung mittels "
                                             "vorangestelltem # zugefügt."))
    materials = models.ManyToManyField(Material, through="MaterialAmount", blank=True,
                                       help_text=("Welche Materialien sind notwendig? "
                                                  "Mengenangaben sind optional."),
                                       verbose_name="Materialien")
    field_of_education = models.ManyToManyField(FieldOfEducation,
                            help_text="Bildungs- und Erziehungsbereiche, die betroffen sind.",
                            verbose_name="Bildungsbereiche")

    def update_tags_from_description(self):
        """
        Search description for hashtags, remove obsolete tags and add new tags
        if necessary.
        """
        new_tags = tuple(match.group(2).lower() for match in RE_HASHTAG.finditer(self.description))
        self.tags.exclude(name__in=new_tags).delete()  # Delete obsolete tags.
        existing_tags = Tag.objects.filter(name__in=new_tags)
        existing_tag_names = tuple(tag.name for tag in existing_tags)
        new_tags = filter(lambda x: x not in existing_tag_names, new_tags)
        new_tags = tuple(Tag.objects.create(name=tag) for tag in new_tags)
        self.tags.add(*new_tags, *existing_tags)

    def save(self, *args, **kwargs):
        """
        Parse tags from description and save them as well as its relations.
        """
        super(Activity, self).save(*args, **kwargs)
        self.update_tags_from_description()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Angebot"
        verbose_name_plural = "Angebote"


class Image(models.Model):
    
    description = models.CharField(max_length=250, blank=True,
                                   help_text="Optional: Kurze Beschreibung mit Maximallänge 250.",
                                   verbose_name="Beschreibung")
    upload = models.ImageField(upload_to=file_upload_path)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE,
                                 verbose_name="Angebot")

    def __str__(self):
        return self.upload.url

    class Meta:
        verbose_name = "Bild"
        verbose_name_plural = "Bilder"


class File(models.Model):
    description = models.CharField(max_length=250, blank=True,
                                   help_text="Optional: Kurze Beschreibung mit Maximallänge 250.",
                                   verbose_name="Beschreibung")
    upload = models.FileField(upload_to=file_upload_path)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE,
                                 verbose_name="Angebot")

    def __str__(self):
        return self.upload.url

    class Meta:
        verbose_name = "Datei"
        verbose_name_plural = "Dateien"


class MaterialAmount(models.Model):
    UNIT_CHOICES = (
        ("", ""),
        ("l", "l"),
        ("ml", "ml"),
        ("g", "g"),
        ("mg", "mg"),
        ("Ta", "Tassen"),
        ("EL", "EL"),
        ("TL", "TL"),
        ("St", "Stück"))

    material = models.ForeignKey(Material, on_delete=models.PROTECT,
                                 verbose_name="Material")
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE,
                                 verbose_name="Angebot")
    amount = models.PositiveIntegerField(default=0,
                                         help_text="Auf 0 lassen falls keine präzise Mengenangabe nötig.",
                                         verbose_name="Menge")
    unit = models.CharField(max_length=2, choices=UNIT_CHOICES, blank=True, default="",
                            help_text="Optional. Falls eine Maßeinheit fehlt bitte beim Administrator melden.",
                            verbose_name="Maßeinheit")

    def __str__(self):
        if self.amount == 0:
            return str(self.material)
        else:
            return "{} {} {}".format(self.amount, self.unit, self.material)

    class Meta:
        verbose_name = "Material und Mengen"
        verbose_name_plural = "Materialien und Mengen"