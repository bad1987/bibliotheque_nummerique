from django.db import models


class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Livre(models.Model):
    description = models.CharField(max_length=255, null=True)
    # document = models.FileField(upload_to='documents/')
    bookname = models.TextField()
    url = models.TextField()
    imagelink = models.TextField()
    catgorie = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Logiciel(models.Model):
    nom = models.CharField(max_length=30,null=False)
    nomFichier = models.CharField(max_length=200,null=False)
    url = models.TextField()
    version = models.CharField(max_length=15)
    dateAjout = models.DateTimeField(auto_now_add=True)
    categorie = models.CharField(max_length=50,blank=True)