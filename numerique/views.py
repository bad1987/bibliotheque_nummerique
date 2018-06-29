from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.conf import settings
import os
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

import subprocess, threading, mimetypes, urllib

from imagecreator import creator
from .forms import DocumentForm, UserRegistrationForm
from .models import Livre, Logiciel

def welcomeIndex(request):
    return render(request, 'numerique/welcome.html',{})

def logiciel(request):
    nom = request.POST.get('nom')
    categorie = request.POST.get('categorie')
    version = request.POST.get('version')
    software = request.FILES['logiciel']
    nomFichier = software.name

    # aff = str(nom) + ' ' + str(categorie) + ' ' + str(version) + ' ' + str(software)
    # print(aff)

    # si le repertoire contenant les logiciels de la categorie n'existe
    # pas,on le cree d'abord
    path = settings.MEDIA_DIR + '/' + 'logiciels/' + categorie

    if not os.path.isdir(path):
        os.mkdir(path)

    # stockage du logiciel dans le systeme de fichier
    fs = FileSystemStorage(location=path)
    filename = fs.save(software.name, software)

    # mise a jour de la base de donnees

    bd = Logiciel(
        nom=nom,
        nomFichier=nomFichier,
        url=path,
        version=version,
        categorie=categorie
    )

    bd.save()

    return render(request, 'numerique/index.html',{'softwareadded':True})

def index(request):
    saved = False
    submited = False

    # slide for picture
    images = os.listdir(settings.STATIC_DIR + '/images/slide')
    num_images = []
    for i in range(len(images)):
        num_images.append(i)

    if request.method == 'POST' and request.FILES['myfile']:
        categorie = request.POST.get('categorie')

        #si le repertoire contenant les livres de la categorie n'existe
        #pas,on le cree d'abord
        path = settings.MEDIA_DIR + '/' + categorie

        if not os.path.isdir(path):
            os.mkdir(path)

            # creation du dossier qui va contenir les versions html
            os.mkdir(os.path.join(path,'htmlversion'))

        submited = True
        myfile = request.FILES['myfile']
        fs = FileSystemStorage(location=path)
        filename = fs.save(myfile.name, myfile)
        # uploaded_file_url = fs.url(filename)
        uploaded_file_url = '/media/' + categorie + '/' + filename

        #on cree l'image pour le fichier
        imagelink = creator(uploaded_file_url, path)
        saved = True


        #creation de la version html
        filepath = uploaded_file_url[1:]
        thread = threading.Thread(target=htmlversion,args=(request,filepath,), daemon=True)
        thread.start()

        #modification de la base de donnees
        bs = Livre(
            bookname=filename,
            url=uploaded_file_url,
            imagelink=imagelink,
            catgorie=categorie
        )

        bs.save()

    return render(request, 'numerique/index.html',{'saved':saved,'submited':submited,'images':images,'num_images':num_images})


def registration(request):

    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)

        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request,'numerique/registrationOk.html',{'new_user':new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,'numerique/registration.html',{'user_form':user_form})


def userLogin(request):
    errors = False
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            login(request,user)
            return HttpResponseRedirect(reverse('index'))
        else:
            errors = True
    return render(request,'numerique/login.html',{'errors':errors})

def userLogout(request):
    logout(request)

    return HttpResponseRedirect(reverse('welcomeIndex'))

def displaySoftware(request ):

    list_softwares = Logiciel.objects.order_by("dateAjout")[:5]

    return render(request, 'numerique/displaysoftwares.html',{"softwares":list_softwares})

def displaySoftwareByCategory(request,categorie):

    # correction de la categorie pour le lien de maintenance
    if str(categorie) == 'maintlogi':
        categorie = 'maintenance'

    list_softwares = Logiciel.objects.filter(categorie=categorie).order_by("dateAjout")
    return render(request, 'numerique/displaysoftwares.html',{"softwares":list_softwares})

def displayBooks(request):

    cat = str(request.META['PATH_INFO']).split('/')[-1]

    #dictionnaire de categories
    dict_cat = {
        'programmation':"Developpement d'application",
        'reseau':"Reseau et Telecom",
        'maintenance':"Maintenance",
    }

    # print(dict_cat[cat])

    list_books = Livre.objects.filter(catgorie=dict_cat[cat])
    paginator = Paginator(list_books,6)
    page = request.GET.get('page')
    try:
        list_books = paginator.page(page)
    except PageNotAnInteger:
        list_books = paginator.page(1)
    except EmptyPage:
        list_books = paginator.page(paginator.num_pages)

    return render(request,'numerique/programmation.html',{'list_books':list_books, 'categorie':dict_cat[cat]})

def reseautelecom(request):

    list_books = Livre.objects.filter(catgorie='reseautelecom')
    paginator = Paginator(list_books, 6)
    page = request.GET.get('page')
    try:
        list_books = paginator.page(page)
    except PageNotAnInteger:
        list_books = paginator.page(1)
    except EmptyPage:
        list_books = paginator.page(paginator.num_pages)

    return render(request,'numerique/programmation.html',{'list_books':list_books,'categorie':'reseautelecom'})

def montageav(request):

    list_books = Livre.objects.filter(catgorie='montageav')
    paginator = Paginator(list_books, 6)
    page = request.GET.get('page')
    try:
        list_books = paginator.page(page)
    except PageNotAnInteger:
        list_books = paginator.page(1)
    except EmptyPage:
        list_books = paginator.page(paginator.num_pages)

    return render(request,'numerique/programmation.html',{'list_books':list_books,'categorie':'montageav'})

def bureatique(request):

    list_books = Livre.objects.filter(catgorie='bureautique')
    paginator = Paginator(list_books, 6)
    page = request.GET.get('page')
    try:
        list_books = paginator.page(page)
    except PageNotAnInteger:
        list_books = paginator.page(1)
    except EmptyPage:
        list_books = paginator.page(paginator.num_pages)

    return render(request,'numerique/programmation.html',{'list_books':list_books,'categorie':'bureautique'})

def systeme(request):

    list_books = Livre.objects.filter(catgorie='systeme')
    paginator = Paginator(list_books, 6)
    page = request.GET.get('page')
    try:
        list_books = paginator.page(page)
    except PageNotAnInteger:
        list_books = paginator.page(1)
    except EmptyPage:
        list_books = paginator.page(paginator.num_pages)

    return render(request,'numerique/programmation.html',{'list_books':list_books,'categorie':'systeme'})

def video(request):
    return render(request,'numerique/video.html',{})

def actualite(request):
    return render(request,'numerique/actualite.html',{})


def simple_upload(request):

    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)

        #on cree l'image pour fichier
        creator(uploaded_file_url)

        return render(request, 'numerique/book-upload.html',{'uploaded_file_url':uploaded_file_url})
    return render(request,'numerique/book-upload.html')


def model_form_upload(request):

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            myfile = request.FILES['document']
            chemin = os.path.join(os.path.join(settings.MEDIA_DIR,'documents'),myfile.name)
            creator(chemin)
            return redirect('index')
    else:
        form = DocumentForm()

    return render(request, 'numerique/model-form-upload.html',{'form':form})


def downloadSoftware(request,link):

    fp = open(link,'rb')

    response = HttpResponse(fp.read())
    fp.close()
    type, encoding = mimetypes.guess_type(link)
    if type is None:
        type = 'application/octet-stream'
    response['Content-Type'] = type
    response['Content-Length'] = str(os.stat(link).st_size)
    if encoding is not None:
        response['Content-Encoding'] = encoding

    # To inspect details for the below code, see http://greenbytes.de/tech/tc2231/
    if u'WebKit' in request.META['HTTP_USER_AGENT']:
        # Safari 3.0 and Chrome 2.0 accepts UTF-8 encoded string directly.
        filename_header = 'filename=%s' % link.encode('utf-8')
    elif u'MSIE' in request.META['HTTP_USER_AGENT']:
        # IE does not support internationalized filename at all.
        # It can only recognize internationalized URL, so we do the trick via routing rules.
        filename_header = ''
    else:
        # For others like Firefox, we follow RFC2231 (encoding extension in HTTP headers).
        # filename_header = 'filename*=UTF-8\'\'%s' % urllib.quote(link.encode('utf-8'))
        filename_header = 'filename*=UTF-8\'\'%s' % urllib.parse.quote(link.encode('utf-8'))

    response['Content-Disposition'] = 'attachment; ' + filename_header

    return response

def anything(request,bookname):

    decoupage = os.path.split(bookname)
    dossier = os.path.join(decoupage[0],'htmlversion')
    name = str(decoupage[1]).split('.')[0] + '.html'
    relatifpath = os.path.join(dossier,name)
    fullpath = os.path.join(os.getcwd(),relatifpath[1:])

    # on verifie si la version html est deja disponible
    contenu = os.listdir(os.path.join(os.getcwd(),dossier[1:]))
    if  not name in contenu:
        return HttpResponse("la version html n'est pas encore disponible")


    livre = ''

    b = ['cat',os.path.join(os.getcwd(),'templates/numerique/block.js')]
    s = subprocess.run(b,stdout=subprocess.PIPE)

    # livre += s.stdout.decode()
    # livre += '<iframe src="' + relatifpath + '"' + ' height="100%" width="100%"></iframe>'
    # livre += s.stdout.decode()

    with open(fullpath,'rb') as f:
        livre = f.read()
    livre = livre.decode() + s.stdout.decode()
    return HttpResponse(livre,content_type='text/html')

    # return render(request,'numerique/displaybooks.html',{'livre':fullpath})
    # return HttpResponse(livre,content_type='text/html')

def htmlversion(request,filepath):

    decouper = os.path.split(filepath)
    #chemin absolue du livre
    file = os.path.join(os.getcwd(),filepath)
    #chemin relatif de la version html
    outputlocation = os.path.join(decouper[0],'htmlversion/' + str(decouper[1]).split('.')[0] + '.html')
    args = ['pdf2htmlEX',file,outputlocation]

    subprocess.run(args)