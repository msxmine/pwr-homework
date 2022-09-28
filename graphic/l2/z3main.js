async function main(){
    //Czekaj na załadowanie textur
    await loadAssets();
    var last_time = performance.now();
    function update(time){
        //Policz czas od ostatniego odświeżenia
        var deltat = time - last_time;
        last_time = time;
        
        handleInput(deltat);
        calculateBall(deltat);
        recalcDynamicVertex();
        reloadDynamicBuffers();
        render();
        //Poproś o ponowne uruchomienie tej funkcji przy rysowaniu kolejnej klatki
        window.requestAnimationFrame(update);
    }
    update(performance.now());
}
main();
