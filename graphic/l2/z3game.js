//Stałe
const paddle_height = 0.3;
const ball_speed = 0.001;
const player_speed = 0.0015;
const ball_radius = 0.03;

//Stan gry
var p1paddle_pos = 0;
var p2paddle_pos = 0;
var ballx = 0;
var bally = 0;
var ballvelx = -ball_speed;
var ballvely = 0;
var score1 = 0;
var score2 = 0;

//Stan wejsc uzytkownikow W/S,GÓRA/ÐÓŁ
var wpressed = false
var spressed = false
var uppressed = false
var downpressed = false

//Dodaj element sledzacy klawisze
canvas = document.getElementById("my_canvas");
canvas.addEventListener("keydown", event => {
    if (event.keyCode === 87){wpressed = true;}
    if (event.keyCode === 83){spressed = true;}
    if (event.keyCode === 38){uppressed = true;}
    if (event.keyCode === 40){downpressed = true;}
}, false);
canvas.addEventListener("keyup", event => {
    if (event.keyCode === 87){wpressed = false;}
    if (event.keyCode === 83){spressed = false;}
    if (event.keyCode === 38){uppressed = false;}
    if (event.keyCode === 40){downpressed = false;}
}, false);

//Przesuwanie paletek w zaleznosci od klawiszy
function handleInput(deltat){
    if (wpressed){
        //Predkosc*czas
        p1paddle_pos += player_speed * deltat;
        //Ograniczenie przez sufit
        p1paddle_pos = ((p1paddle_pos+(paddle_height/2) < 1) ? p1paddle_pos : (1 - (paddle_height/2)));
    }
    if (spressed){
        p1paddle_pos -= player_speed * deltat;
        p1paddle_pos = ((p1paddle_pos-(paddle_height/2) > -1) ? p1paddle_pos : (-1 + (paddle_height/2)));
    }
    if (uppressed){
        p2paddle_pos += player_speed * deltat;
        p2paddle_pos = ((p2paddle_pos+(paddle_height/2) < 1) ? p2paddle_pos : (1 - (paddle_height/2)));
    }
    if (downpressed){
        p2paddle_pos -= player_speed * deltat;
        p2paddle_pos = ((p2paddle_pos-(paddle_height/2) > -1) ? p2paddle_pos : (-1 + (paddle_height/2)));
    }
}

//Liczenie pozycji piłki
function calculateBall(deltat){
    //Zwykłe przesunięcie
    let deltax = deltat*ballvelx;
    let deltay = deltat*ballvely;
    let newballx = ballx+deltax;
    let newbally = bally+deltay;
    
    //Zderzenie z lewą ścianą
    if (newballx-ball_radius < -1){
        //Policz część ruchu przed ścianą
        let inspacefrac = Math.abs(((ballx-ball_radius)+1)/deltax);
        //Policz współrzędną Y zderzenia, wiedząc że prędkość jest stała
        let impacty = bally+(deltay*inspacefrac);
        //Sprawdz czy gracz 1 zablokował piłeczke
        if (impacty < (p1paddle_pos + (paddle_height/2)) && impacty > (p1paddle_pos - (paddle_height/2))){
            //Jesli tak to policz nachylenie wektora predkosci przed zderzeniem
            let ball_angle = Math.atan2(ballvely, ballvelx) + Math.PI;
            //Policz krzywizne paletki (Odchylenie od pionu na wysokości zderzenia)
            let paddle_curve = ((impacty - p1paddle_pos)/(paddle_height/2))*(Math.PI/12)
            //Kat odbicia = kat padania
            let new_angle = (2*paddle_curve)-ball_angle;
            //Obroc wektor predkosci do nowego nachylenia
            ballvelx = Math.cos(new_angle)*ball_speed;
            ballvely = Math.sin(new_angle)*ball_speed;
            //Policz czesc ruchu z nowymi predkosciami i zaktualizuj pozycje od miejsca zderzenia
            newballx = -1 + ball_radius + (deltat*ballvelx*(1-inspacefrac));
            newbally = impacty + (deltat*ballvely*(1-inspacefrac));
        }
        //Jesli nie to nabij punkt dla gracza 2 i zresetuj plansze
        else{
            score2++;
            ballvely = 0;
            ballvelx = ball_speed;
            newballx = 0;
            newbally = 0;
        }
    }
    //Zderzenie z prawą ścianą
    if (newballx+ball_radius > 1){
        let inspacefrac = Math.abs(((ballx+ball_radius)-1)/deltax);
        let impacty = bally+(deltay*inspacefrac);
        if (impacty < (p2paddle_pos + (paddle_height/2)) && impacty > (p2paddle_pos - (paddle_height/2))){
            let ball_angle = Math.atan2(ballvely, ballvelx) + Math.PI;
            let paddle_curve = (((p2paddle_pos - impacty)/(paddle_height/2))*(Math.PI/12))+Math.PI;
            let new_angle = (2*paddle_curve)-ball_angle;
            ballvelx = Math.cos(new_angle)*ball_speed;
            ballvely = Math.sin(new_angle)*ball_speed;
            newballx = 1 - ball_radius + (deltat*ballvelx*(1-inspacefrac));
            newbally = impacty + (deltat*ballvely*(1-inspacefrac));
        }
        else{
            score1++;
            ballvely = 0;
            ballvelx = -ball_speed;
            newballx = 0;
            newbally = 0;
        }
    }
    //Zderzenie z dolną ścianą
    if (newbally-ball_radius < -1){
        //Odbij prędkość pionową
        ballvely = Math.abs(ballvely);
        //Policz głębokość zderzenia i odbij
        newbally = -1 + ball_radius + Math.abs((newbally-ball_radius) + 1);
    }
    //Zderzenie z górną ścianą
    if (newbally+ball_radius > 1){
        ballvely = -Math.abs(ballvely);
        newbally = 1 - ball_radius - Math.abs((newbally+ball_radius) - 1);
    }
    //Zastosuj zmiany pozycji
    ballx = newballx;
    bally = newbally;
}
