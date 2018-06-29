from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$',views.welcomeIndex,name='welcomeIndex'),
    url(r'^index',views.index,name='index'),
    url(r'^logiciel',views.logiciel,name='logiciel'),
    url(r'^displaysoftware',views.displaySoftware,name='displaysoftware'),
    url(r'^categorielogiciel/(?P<categorie>.*?)/$',views.displaySoftwareByCategory,name='categorielogiciel'),
    url(r'^programmation',views.displayBooks,name='programmation'),
    url(r'^reseau',views.displayBooks,name='reseau'),
    # url(r'^montageav',views.montageav,name='montageav'),
    # url(r'^bureautique',views.bureatique,name='bureautique'),
    url(r'^video',views.video,name='video'),
    url(r'^registration',views.registration,name='registration'),
    url(r'^userLogin',views.userLogin,name='userLogin'),
    url(r'^userLogout',views.userLogout,name='userLogout'),
    url(r'actualite',views.actualite,name='actualite'),
    url(r'^maintenance',views.displayBooks,name='maintenance'),
    # url(r'^book-upload',views.simple_upload,name='book-upload'),
    url(r'^anything(?P<bookname>.*?)/$',views.anything,name='anything'),
    url(r'^download(?P<link>.*?)/$',views.downloadSoftware,name='download'),
    # url(r'^categorielogiciel/[\w*?]/download(?P<link>.*?)/$',views.downloadSoftware,name='download'),
]