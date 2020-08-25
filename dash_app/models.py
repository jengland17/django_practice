from django.db import models
import re
import bcrypt

# Create your models here.

class UserManager(models.Manager):

    def register_validator(self, postData):

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        errors = {}

        if len(postData['form_first']) < 3:
            errors['firstname_req'] = "First Name is required and must be at least 3 characters"

        if len(postData['form_last']) < 3:
            errors['lastname_req'] = "Last Name is required and must be at least 3 characters"

        if len(postData['form_email']) == 0:
            errors['email_req'] = "Email is required"
        elif not EMAIL_REGEX.match(postData['form_email']):
            errors['valid_email'] = "Must be a valid email"
        else:
            repeat_email = User.objects.filter(email = postData['form_email'])
            if len(repeat_email) > 0:
                errors['taken_email'] = "This email has already been used"

        if len(postData['password']) < 8:
            errors['pass_req'] = "Password is required and must be at leats 8 characters"
        if postData['password'] != postData['confirm_pass']:
            errors['confirm_req'] = "Password must match"

        return errors
    
    def login_validator(self, postData):

        match_email = User.objects.filter(email = postData['form_email'])
        
        errors = {}

        if len(postData['form_email']) == 0:
            errors['email_req'] = "Email is required to login"
            
        elif len(match_email) == 0:
            errors['email_not_found'] = "Email not found"

        else:

            if bcrypt.checkpw(postData['password'].encode(), match_email[0].password.encode()):
                print('Password Match')
            else:
                errors['wrong_pass'] = "Incorrect password"

        return errors

    def edit_validator(self, postData):

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        errors = {}

        if len(postData['form_first']) < 3:
            errors['firstname_req'] = "First Name is required and must be at least 3 characters"

        if len(postData['form_last']) < 3:
            errors['lastname_req'] = "Last Name is required and must be at least 3 characters"

        if len(postData['form_email']) == 0:
            errors['email_req'] = "Email is required"
        elif not EMAIL_REGEX.match(postData['form_email']):
            errors['valid_email'] = "Must be a valid email"
        
        return errors



class PostManager(models.Manager):
    
    def post_validator(self, postData):

        errors = {}

        if len(postData['form_author']) < 3:
            errors['author_req'] = "Please provide an author and must be at least 3 characters"
        if len(postData['form_quote']) < 10:
            errors['quote_req'] = "Please provide a quote that is at least 10 characters"
    
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Post(models.Model):
    author = models.CharField(max_length=255)
    quote = models.CharField(max_length=255)
    users = models.ManyToManyField(User, related_name="quotes")
    uploader = models.ForeignKey(User, related_name="uploaded_quote", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = PostManager()
