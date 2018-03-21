from django.db import models

class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)
    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)

class UserType(models.Model):
    user_type = models.CharField(max_length=255, verbose_name='User Type')

    def __str__(self):
        return self.user_type
    def __unicode__(self):
        return self.title

class User(models.Model):
    name = models.CharField(max_length=255, verbose_name='User Name', null=False)
    user_type = models.ForeignKey(UserType, on_delete=None, null=False)
    user_address = models.TextField(max_length=1000, verbose_name='Address', null=False)
    contact_details_1 = models.CharField(max_length=13, verbose_name='Phone Number 1', null=False)
    contact_details_2 = models.CharField(max_length=13, verbose_name='Phone Number 2', null=True)
    email = models.CharField(max_length=255, verbose_name='EMail ID', null=False)
    rating = IntegerRangeField(help_text='Rating of the User', min_value=1, max_value=10)

    def __unicode__(self):
        return self.title

    def clean(self):
        if rating > 10 or rating < 1:
            raise ValidationError("Rating must be between 1 to 10")
        super(User,self).clean()