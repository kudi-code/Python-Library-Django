import uuid as uuid # Identificador único
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Models
class Book(models.Model):
    ISBN= models.CharField(max_length=100, null=False)
    title = models.CharField(max_length=80, null=False)
    author = models.CharField(max_length=80, null=False)
    subject= models.CharField(null=False, max_length=50)
    publisher= models.CharField(max_length=100,null=False)    
    description = models.TextField()
    language= models.TextField(default="Spanish")
    numberOfPages = models.IntegerField(null=False)
    def __str__(self):
        return  self.title


class BookItem(models.Model):
    BookFormat = [
        ("H", "Hardcover"),
        ("P", "Paperback"),
        ("A", "Audiobooks"),
        ("E", "Ebook"),
        ("N", "Newspaper"),
        ("M", "Magazine"),
        ("J", "Journal"),
    ]

    barcode= models.CharField(max_length=100, null=False)
    isReferenceOnly= models.BooleanField()
    borrowed= models.DateField(null=False)
    dueDate= models.DateField(null=False)
    price= models.FloatField(null=False)
    format= models.CharField(choices=BookFormat, max_length=20)
    dateOfPurchase= models.DateField(null=False)
    publicationDate= models.DateField(null=False)

    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=False)
    member = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4())
    is_rent = models.BooleanField(default=False)
    is_reserve = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)

    def __str__(self) -> str:
        return "Copia de: " + self.book.title + " --- id: " + str(self.id)

@receiver(post_save, sender=BookItem)
def update_available(sender, instance, **kwargs):
    if not kwargs["created"]:
        if instance.is_rent:
            is_available = False
        else:
            is_available =True

        BookItem.objects.filter(pk=instance.id).update(is_available=is_available)
