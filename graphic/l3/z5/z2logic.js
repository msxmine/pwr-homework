func1 = {}
func2 = {}

//Wartosci funkcji
func1.results = []
func2.results = []
//Wektory normalne (srednie w wierzcholkach)
func1.normals = []
func2.normals = []
//Nazwy pol tekstowych
func1.tfid = "function"
func2.tfid = "function2"

//zakresy na osiach
var scale = 0.1

//Indexy wierzcholkow trojkatow powierzchni
surface_idx = []

//Wygeneruj liste indeksow do przyblizenia powierzchni trojkatami
for (i = 0; i < 500; i++){
    for (j = 0; j < 500; j++){
        surface_idx.push(501*j + i, 501*j + i + 1, 501*(j+1) + i )
        surface_idx.push(501*j+i+1, 501*(j+1)+i+1, 501*(j+1)+i )
    }
}

//Iloczyn wektorowy
function vectorcross(edge1, edge2){
    return [edge1[1]*edge2[2] - edge1[2]*edge2[1], edge1[2]*edge2[0] - edge1[0]*edge2[2], edge1[0]*edge2[1]-edge1[1]*edge2[0]]
}

//Kopiowanie vec3 z wiekszej tablicy
function extractvect(array, baseaddr){
    return [ array[baseaddr] , array[baseaddr+1], array[baseaddr+2]]
}

//Roznica vec3
function diffvect(vect1, vect2){
    return [ vect1[0]-vect2[0], vect1[1]-vect2[1], vect1[2]-vect2[2] ]
}

//Dodaj do zapisanej normalnej
function addnormal(addr, normal, func){
    func.normals[addr] += normal[0]
    func.normals[addr+1] += normal[1]
    func.normals[addr+2] += normal[2]
}

//Zmien dlugosc wektora na 1 ale zachowaj kierunek
function normalize(vect){
    let len = Math.sqrt( Math.pow(vect[0],2) + Math.pow(vect[1],2) + Math.pow(vect[2],2))
    return [vect[0]/len, vect[1]/len, vect[2]/len]
}

//Policz wartosci funkcji uzytkownika w punktach kratowych
function calculate(func){
    //Zresetuj zapisane dane
    func.results = []
    func.normals = []
    //Zainicjalizuj tablice wektorow normalnych na 0
    for (i = 0; i <= 500; i++){
        for (j = 0; j <= 500; j++){
            func.normals.push(0,0,0)
        }
    }
    //Znajdz pole tekstowe i pobierz tekst funkcji
    let functionfield = document.getElementById(func.tfid)
    let functiontext = "return (" + functionfield.value + ")"
    //Stworz funkcje jako obiekt JS
    let functionobj = new Function("x", "y", functiontext)

    //Policz wartosci w punktach i zapisz
    for (i = -250; i <= 250; i++){
        for (j = -250; j <= 250; j++){
            let x = (i/250)
            let y = (j/250)
            let z = functionobj(x/scale,y/scale)*scale
            func.results.push(x,z,-y)
        }
    }

    //Wylicz srednie normalne na wierzcholkach
    for (i = 0; i < 500; i++){
        for (j = 0; j < 500; j++){
            //Trojkat 1
            //adresy w tablicy wierzcholkow trojkata
            let aaddr = 3*(501*j + i)
            let baddr = 3*(501*j + i + 1)
            let caddr = 3*(501*(j+1) + i)
            //Dwie krawedzie
            let edge1 = diffvect(extractvect(func.results, caddr), extractvect(func.results, aaddr))
            let edge2 = diffvect(extractvect(func.results, baddr), extractvect(func.results, aaddr))
            //Iloczyn wektorowy = normalna (wazona)
            let cross = vectorcross(edge1, edge2)
            addnormal(aaddr, cross, func)
            addnormal(baddr, cross, func)
            addnormal(caddr, cross, func)
            //Trojkat 2
            aaddr = 3*(501*j+i+1)
            baddr = 3*(501*(j+1)+i+1)
            caddr = 3*(501*(j+1)+i )
            edge1 = diffvect(extractvect(func.results, caddr), extractvect(func.results, aaddr))
            edge2 = diffvect(extractvect(func.results, baddr), extractvect(func.results, aaddr))
            cross = vectorcross(edge1, edge2)
            addnormal(aaddr, cross, func)
            addnormal(baddr, cross, func)
            addnormal(caddr, cross, func)
            
        }
    }

    //Zamien normalne wazone na prawdziwe (o dl. 1)
    for (i = 0; i <=500; i++){
        for (j = 0; j <= 500; j++){
            let realnormal = normalize(extractvect(func.normals, 3*(i*501 + j )))
            func.normals[3*(i*501 + j ) + 0] = realnormal[0]
            func.normals[3*(i*501 + j ) + 1] = realnormal[1]
            func.normals[3*(i*501 + j ) + 2] = realnormal[2]
            
        }
    }

}
//Policz raz przy ladowaniu
calculate(func1)
calculate(func2)

//Licz ponownie przy nacisnieciu guzika
document.getElementById("draw").addEventListener("click", function() {
    calculate(func1)
    updateBufs()
});

//Licz ponownie przy nacisnieciu guzika g(x,y)
document.getElementById("draw2").addEventListener("click", function() {
    calculate(func2)
    updateBufs()
});
