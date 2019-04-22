import reversion

from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()


@reversion.register()
class School(models.Model):
    full_name = models.CharField(max_length=255)
    participants = models.ManyToManyField(
        User,
        through='Participation',
        through_fields=('school', 'user'),
        related_name="participants"
    )
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    grade = models.IntegerField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    zip_code = models.IntegerField(null=True, blank=True)
    application_reviews_required = models.IntegerField(help_text="Reviews required for each application received",
                                                       default=3)

    def __str__(self):
        return self.full_name


@reversion.register()
class Staff(models.Model):
    user = models.OneToOneField(User, primary_key=False, related_name='staff',
                                on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.IntegerField(null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.first_name


@reversion.register()
class Participation(models.Model):
    PARTICIPATION_OWNER = 'o'
    PARTICIPATION_STAFF = 's'
    PARTICIPATION_CHOICES = (
        (PARTICIPATION_OWNER, 'Owner'),
        (PARTICIPATION_STAFF, 'Staff'),
    )
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='participation')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='participation')
    participation_date = models.DateTimeField()
    participation_type = models.CharField('Participation', max_length=1, choices=PARTICIPATION_CHOICES)

    def __str__(self):
        return self.participation_type


@reversion.register()
class Invite(models.Model):
    INVITATION_PENDING = 'p'
    INVITATION_ACCEPT = 'a'
    INVITATION_CHOICES = (
        (INVITATION_PENDING, 'Pending'),
        (INVITATION_ACCEPT, 'Accept'),
    )

    username = models.CharField(max_length=255, null=True, blank=True)
    school = models.ForeignKey(
        School,
        related_name='invite',
        on_delete=models.CASCADE
    )
    email = models.CharField(max_length=255, null=True, blank=True)
    invitation_date = models.DateTimeField()
    acceptation_date = models.DateTimeField(null=True)
    status = models.CharField('Status', max_length=1, choices=INVITATION_CHOICES)

    def __str__(self):
        return self.username


@reversion.register()
class Season(models.Model):
    full_name = models.CharField(max_length=255)
    school = models.ForeignKey(
        School,
        related_name='season',
        on_delete=models.CASCADE
    )
    kind = models.CharField(max_length=255, null=True, blank=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    info = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.full_name


@reversion.register()
class Application(models.Model):
    GENDER_UNKNOWN = 'u'
    GENDER_MALE = 'm'
    GENDER_FEMALE = 'f'
    GENDER_CHOICES = (
        (GENDER_UNKNOWN, 'Unknown'),
        (GENDER_MALE, 'Male'),
        (GENDER_FEMALE, 'Female'),
    )

    STATUS_PENDING = 'p'
    STATUS_REVIEWED = 'r'
    STATUS_ENROLLED = 'e'
    STATUS_CHOICES = (
        (STATUS_PENDING, 'Pending'),
        (STATUS_REVIEWED, 'Reviewed'),
        (STATUS_ENROLLED, 'Enrolled'),
    )

    # bulkApplicationFile = models.ForeignKey(
    #     BulkApplicationFile,
    #     related_name='bulkFile',
    #     on_delete=models.CASCADE()
    # )
    season = models.ForeignKey(
        Season,
        related_name='application',
        on_delete=models.CASCADE
    )

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    birth_date = models.DateField('Date of birth', blank=True, null=True)
    gender = models.CharField('Gender', max_length=1, choices=GENDER_CHOICES, default=GENDER_UNKNOWN)
    phone_number = models.IntegerField(null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    info = models.CharField(max_length=255, null=True, blank=True)
    educational_info = models.CharField(max_length=255, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField('Status', max_length=1, choices=STATUS_CHOICES, default=STATUS_PENDING)

    def __str__(self):
        return self.first_name


@reversion.register()
class BulkApplicationFile(models.Model):
    user = models.ForeignKey(
        User,
        related_name='applicationsFile',
        on_delete=models.CASCADE
    )
    uploadDate = models.DateField('Upload Date', blank=True, null=True)
    fileContent = models.FileField(upload_to='uploadedApplications')
    success = models.BooleanField(default=False)


@reversion.register()
class Review(models.Model):
    application = models.ForeignKey(
        Application,
        related_name='review',
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)

    review_date = models.DateTimeField(auto_now_add=True, null=True)
    score = models.IntegerField(null=True, blank=True)
    note = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.review_date.strftime("%H:%M:%S.%f - %b %d %Y")
