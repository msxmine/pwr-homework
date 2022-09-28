package com.example.pong

class PongGame {
    val paddle_height = 0.3f;
    val ball_speed = 0.001f;
    val player_speed = 0.0015f;
    val ball_radius = 0.0f;

    //Stan gry
    @Volatile var p1paddle_pos = 0f;
    @Volatile var p2paddle_pos = 0f;
    @Volatile var ballx = 0f;
    @Volatile var bally = 0f;
    @Volatile var ballvelx = -ball_speed;
    @Volatile var ballvely = 0f;
    @Volatile var score1 = 0f;
    @Volatile var score2 = 0f;

    @Volatile var wpressed = false
    @Volatile var spressed = false
    @Volatile var uppressed = false
    @Volatile var downpressed = false

    //Przesuwanie paletek w zaleznosci od klawiszy
    fun handleInput(deltat : Float){
        if (wpressed){
            //Predkosc*czas
            p1paddle_pos += player_speed * deltat;
            //Ograniczenie przez sufit
            p1paddle_pos = if(p1paddle_pos+(paddle_height/2) < 1)  p1paddle_pos else (1 - (paddle_height/2))
        }
        if (spressed){
            p1paddle_pos -= player_speed * deltat;
            p1paddle_pos = if(p1paddle_pos-(paddle_height/2) > -1)  p1paddle_pos else (-1 + (paddle_height/2))
        }
        if (uppressed){
            p2paddle_pos += player_speed * deltat;
            p2paddle_pos = if(p2paddle_pos+(paddle_height/2) < 1)  p2paddle_pos else (1 - (paddle_height/2))
        }
        if (downpressed){
            p2paddle_pos -= player_speed * deltat;
            p2paddle_pos = if(p2paddle_pos-(paddle_height/2) > -1)  p2paddle_pos else (-1 + (paddle_height/2))
        }
    }

    //Liczenie pozycji piłki
    fun calculateBall(deltat: Float){
        //Zwykłe przesunięcie
        var deltax = deltat*ballvelx;
        var deltay = deltat*ballvely;
        var newballx = ballx+deltax;
        var newbally = bally+deltay;

        //Zderzenie z lewą ścianą
        if (newballx-ball_radius < -1){
            //Policz część ruchu przed ścianą
            var inspacefrac = Math.abs(((ballx-ball_radius)+1)/deltax);
            //Policz współrzędną Y zderzenia, wiedząc że prędkość jest stała
            var impacty = bally+(deltay*inspacefrac);
            //Sprawdz czy gracz 1 zablokował piłeczke
            if (impacty < (p1paddle_pos + (paddle_height/2)) && impacty > (p1paddle_pos - (paddle_height/2))){
                //Jesli tak to policz nachylenie wektora predkosci przed zderzeniem
                var ball_angle = Math.atan2(ballvely.toDouble(), ballvelx.toDouble()) + Math.PI;
                //Policz krzywizne paletki (Odchylenie od pionu na wysokości zderzenia)
                var paddle_curve = ((impacty - p1paddle_pos)/(paddle_height/2))*(Math.PI/12)
                //Kat odbicia = kat padania
                var new_angle = (2*paddle_curve)-ball_angle;
                //Obroc wektor predkosci do nowego nachylenia
                ballvelx = (Math.cos(new_angle)*ball_speed).toFloat();
                ballvely = (Math.sin(new_angle)*ball_speed).toFloat();
                //Policz czesc ruchu z nowymi predkosciami i zaktualizuj pozycje od miejsca zderzenia
                newballx = -1 + ball_radius + (deltat*ballvelx*(1-inspacefrac));
                newbally = impacty + (deltat*ballvely*(1-inspacefrac));
            }
            //Jesli nie to nabij punkt dla gracza 2 i zresetuj plansze
            else{
                score2++;
                ballvely = 0f;
                ballvelx = ball_speed;
                newballx = 0f;
                newbally = 0f;
            }
        }
        //Zderzenie z prawą ścianą
        if (newballx+ball_radius > 1){
            var inspacefrac = Math.abs(((ballx+ball_radius)-1)/deltax);
            var impacty = bally+(deltay*inspacefrac);
            if (impacty < (p2paddle_pos + (paddle_height/2)) && impacty > (p2paddle_pos - (paddle_height/2))){
                var ball_angle = Math.atan2(ballvely.toDouble(), ballvelx.toDouble()) + Math.PI;
                var paddle_curve = (((p2paddle_pos - impacty)/(paddle_height/2))*(Math.PI/12))+Math.PI;
                var new_angle = (2*paddle_curve)-ball_angle;
                ballvelx = (Math.cos(new_angle)*ball_speed).toFloat();
                ballvely = (Math.sin(new_angle)*ball_speed).toFloat();
                newballx = 1 - ball_radius + (deltat*ballvelx*(1-inspacefrac));
                newbally = impacty + (deltat*ballvely*(1-inspacefrac));
            }
            else{
                score1++;
                ballvely = 0f;
                ballvelx = -ball_speed;
                newballx = 0f;
                newbally = 0f;
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


}