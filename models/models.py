from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    thumbnail = models.ImageField(upload_to='img/thumbnail/')
    image = models.ImageField(upload_to='img/')
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1023)
    price = models.IntegerField()
    status = models.CharField(max_length=255)
    is_visible = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User)
    product = models.ForeignKey(Product)
    quantity = models.IntegerField()
    datetime = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username

class GitRepository(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=127)
    full_name = models.CharField(max_length=1023)
    is_connected = models.BooleanField(default=False)

class RepositoryUpdate(models.Model):
    user = models.ForeignKey(User)
    started_at = models.DateTimeField(auto_now=True)
    is_processed = models.BooleanField(default=False)

class company_model(Base):
        __tablename__ = 'companies'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    address_id = Column(Integer, ForeignKey('addresses.id'))
    address = relationship(Address)

class category_model(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)