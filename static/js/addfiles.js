function livre(){
    document.getElementById("livre").style.display="inline-block";
    document.getElementById("logiciel").style.display="none";
}

function logiciel(){
    document.getElementById("livre").style.display="none";
    document.getElementById("logiciel").style.display="inline-block";
}

function checklivre() {

    // initialisation
    document.getElementById("alertlivre").innerHTML="";
    var content = document.getElementById("inputfile").value;
    if (content == "") {

        // alert("vous devez selectionner un livre");
        error = document.getElementById("alertlivre");
        error.innerHTML="vous devez selectionner un livre";
        error.style.backgroundColor = "red";
        error.style.fontFamily = "Verdana";
        return false;
    }
    return true;
 }

function checklogiciel() {

    // initialisation
    document.getElementById("alertnom").innerHTML="";
    document.getElementById("alertlogiciel").innerHTML="";

    var content = document.getElementById("software").value;
    var correct = true;
    if (content == "") {
        // alert("vous devez selectionner un livre");
        var error = document.getElementById("alertlogiciel");
        error.innerHTML="veillez selectionner un logiciel";
        error.style.backgroundColor = "red";
        error.style.fontFamily = "Verdana";
        correct = false;
    }

    var nom = document.getElementById("nom").value;
    if (nom == "") {
        // alert("vous devez selectionner un livre");
        var errornom = document.getElementById("alertnom");
        errornom.innerHTML="veillez renseigner le nom du logiciel";
        errornom.style.backgroundColor = "red";
        errornom.style.fontFamily = "Verdana";
        correct = false;
    }

    return correct;
}

