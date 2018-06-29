import PyPDF2
from wand.image import Image
import os
from django.conf import settings



def creator(fichierSource, path):

    #le chemin doit etre absolue
    if not '/home' in fichierSource:
        fichierSource = os.path.join(str(os.getcwd()),fichierSource)
    base = os.path.splitext(fichierSource)[0]


    #dans un lien http les espaces sont remplaces par %20. il faut donc les supprimers pour bien travailler
    base = base.replace('%20',' ')

    source = None
    try:
        source = open(base + '.pdf', 'rb')
    except FileNotFoundError:
        base = force(path)
        source = open(base + '.pdf', 'rb')

    outputnamecopy = base + 'copy.pdf'
    outputnameimage = base + '.jpg'

    fullpathimage = os.path.split(outputnameimage)
    fullpathimage = os.path.join(os.path.join(settings.MEDIA_DIR,'images'),fullpathimage[-1])



    lecteurSource = PyPDF2.PdfFileReader(source)

    #si le fichier est crypte, on le decrypte d'abord
    if lecteurSource.isEncrypted:
        lecteurSource.decrypt('')

    firstpage = lecteurSource.getPage(0)
    cible = open(outputnamecopy, 'wb')

    redacteurCible = PyPDF2.PdfFileWriter()
    redacteurCible.addPage(firstpage)
    redacteurCible.write(cible)
    cible.close()
    source.close()

    with Image(filename=outputnamecopy) as img:
        with img.convert('jpg') as converted:
            converted.save(filename=fullpathimage)

    os.remove(outputnamecopy)

    return os.path.split(outputnameimage)[-1]


def force(path):

    # directory = settings.MEDIA_DIR
    directory = path
    image_dir = os.path.join(settings.MEDIA_DIR, 'images')

    image_base = []
    for image in os.listdir(image_dir):
        if image.endswith('.jpg'):
            image_base.append(os.path.splitext(image)[0])

    pdf_base = []
    for pdf in os.listdir(directory):
        if pdf.endswith('.pdf'):
            pdf_base.append(os.path.splitext(pdf)[0])


    # recherche du pdf qui ne contient pas d'image

    for pdf in pdf_base:
        if pdf not in image_base:
            base = os.path.join(directory,pdf)
            return base




