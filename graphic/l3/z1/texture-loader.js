//Stworzone tekstury
registered_textures = []
//Wybrana przez uzytkownika tekstura
selected_tex = 0

//Tworzenie tekstury gl
function my_createTexture(gl, textype, name){
    var textureId = gl.createTexture();
    gl.activeTexture(gl.TEXTURE0+0);
    gl.bindTexture(textype, textureId);
    //Domyslnie ustaw LINEAR i rozciaganie krawedzi
    gl.texParameteri(textype, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
    gl.texParameteri(textype, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
    gl.texParameteri(textype, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
    gl.texParameteri(textype, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
    var texdet = {}
    texdet["name"] = name
    texdet["id"] = textureId
    texdet["type"] = textype
    //dodaj do stworzonych
    registered_textures.push(texdet)
    refresh_selector(gl)
    return textureId;
}

//Zaladuj teksture z pliku do gl
async function my_loadTexture(gl, texid, textype, texsubtype, url ){
    const image = new Image();
    let aret = new Promise(resolve => {
        image.onload = function(){
            //Po załadowaniu do pamięci, zbinduj do GL
            gl.activeTexture(gl.TEXTURE0)
            gl.bindTexture(textype, texid);
            gl.texImage2D(texsubtype, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, image);
            //Tworzenie mipmap
            gl.generateMipmap(textype);
            resolve(1);
        }
        image.src = url;
    });
    return aret;
}

//Odswierz interfejs uzytkownika
function refresh_selector(gl){
    //Tlumaczenie Obiekt GL -> String nazw filtrow
    var names = {}
    names[gl.LINEAR] = "LINEAR"
    names[gl.NEAREST] = "NEAREST"
    names[gl.NEAREST_MIPMAP_NEAREST] = "NEAREST_MIPMAP_NEAREST"
    names[gl.LINEAR_MIPMAP_NEAREST] = "LINEAR_MIPMAP_NEAREST"
    names[gl.NEAREST_MIPMAP_LINEAR] = "NEAREST_MIPMAP_LINEAR"
    names[gl.LINEAR_MIPMAP_LINEAR] = "LINEAR_MIPMAP_LINEAR"

    //Napisy html
    let textind = document.getElementById("texind")
    let downind = document.getElementById("downind")
    let upind = document.getElementById("upind")

    let cur_texture = registered_textures[selected_tex]
    textind.innerText = "Tekstura : " + cur_texture["name"]

    //Sprawdz obecne filtry i wpisz do html
    gl.bindTexture(cur_texture["type"], cur_texture["id"])
    let cur_down_scaler = gl.getTexParameter(cur_texture["type"], gl.TEXTURE_MIN_FILTER)
    let cur_up_scaler = gl.getTexParameter(cur_texture["type"], gl.TEXTURE_MAG_FILTER)
    downind.innerText = "Skaler pomn. : " + names[cur_down_scaler]
    upind.innerText = "Skaler pow. : " + names[cur_up_scaler]
}

//Zmiany filtrow / wybranej tekstury
function my_onKeyDown(e, gl){
    //Lista dostepnych w WebGL 1 z mipmapami
    downscalers = [gl.LINEAR, gl.NEAREST, gl.NEAREST_MIPMAP_NEAREST, gl.NEAREST_MIPMAP_LINEAR, gl.LINEAR_MIPMAP_NEAREST, gl.LINEAR_MIPMAP_LINEAR]
    upscalers = [gl.LINEAR, gl.NEAREST]

    //Załaduj aktualne, aby wiedziec ktore sa poprzednie/nastepne
    let cur_texture = registered_textures[selected_tex]
    gl.bindTexture(cur_texture["type"], cur_texture["id"])
    let cur_down_scaler = gl.getTexParameter(cur_texture["type"], gl.TEXTURE_MIN_FILTER)
    let cur_up_scaler = gl.getTexParameter(cur_texture["type"], gl.TEXTURE_MAG_FILTER)

    //Filtry powiększające
    if(e.key == "w"){
        gl.texParameteri(cur_texture["type"], gl.TEXTURE_MAG_FILTER, upscalers[ (upscalers.indexOf(cur_up_scaler)+upscalers.length-1)%upscalers.length ]);
    }
    if(e.key == "s"){
        gl.texParameteri(cur_texture["type"], gl.TEXTURE_MAG_FILTER, upscalers[ (upscalers.indexOf(cur_up_scaler)+upscalers.length+1)%upscalers.length ]);
    }
    //Filtry pomniejszające
    if(e.key == "q"){
        gl.texParameteri(cur_texture["type"], gl.TEXTURE_MIN_FILTER, downscalers[ (downscalers.indexOf(cur_down_scaler)+downscalers.length-1)%downscalers.length ]);
    }
    if(e.key == "e"){
        gl.texParameteri(cur_texture["type"], gl.TEXTURE_MIN_FILTER, downscalers[ (downscalers.indexOf(cur_down_scaler)+downscalers.length+1)%downscalers.length ]);
    }
    //Zmien wybrana teksture o 1
    if(e.key == "a"){
        selected_tex = (registered_textures.length+selected_tex-1)%registered_textures.length
    }
    if(e.key == "d"){
        selected_tex = (registered_textures.length+selected_tex+1)%registered_textures.length
    }
    refresh_selector(gl)
}
