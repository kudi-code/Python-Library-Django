from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from books.models import BookItem


class Rack(models.Model):
    rack_number = models.IntegerField()
    locationIdentifier = models.CharField(max_length=200,null=False)


    def __str__(self):
        return  f"{self.locationIdentifier} ---- hall {self.rack_number}"

class RackBookItem(models.Model):
    rack = models.ForeignKey(Rack, on_delete=models.CASCADE)
    book_item = models.ForeignKey(BookItem, on_delete=models.CASCADE)
    floor = models.IntegerField()

    def __str__(self):
        return f" hall {self.rack.rack_number} --- {self.book_item.book.title}"