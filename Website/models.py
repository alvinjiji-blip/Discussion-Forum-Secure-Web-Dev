from django.db import models

class RegisterDB(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # Store hashed passwords using make_password
    full_name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    cover_photo = models.ImageField(upload_to='cover_photos/', blank=True, null=True)

    def __str__(self):
        return self.username  # Fixed duplicate __str__
class CategoryDB(models.Model):
    Cat_Name = models.CharField(max_length=255, unique=True)
    Cat_Image = models.ImageField(upload_to='category_images/', blank=True, null=True)

    def __str__(self):
        return self.Cat_Name
class Post(models.Model):
    user = models.ForeignKey(RegisterDB, on_delete=models.CASCADE)
    category = models.ForeignKey(CategoryDB, on_delete=models.SET_NULL, null=True, blank=True)
    caption = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    video = models.FileField(upload_to='post_videos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(RegisterDB, on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(RegisterDB, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class UserProfile(models.Model):
    user = models.OneToOneField(RegisterDB, on_delete=models.CASCADE)  # Fixed FK reference
    bio = models.TextField(blank=True, null=True)
    place = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], blank=True, null=True)

    def __str__(self):
        return self.user.username


class CategoryRequest(models.Model):
    user = models.ForeignKey(RegisterDB, on_delete=models.CASCADE)  # Reference to RegisterDB
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="category_requests/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} by {self.user.username}"  # Display username from RegisterDB
