package com.example.pong.data

import androidx.room.Entity
import androidx.room.PrimaryKey
import com.example.pong.PongGame

@Entity
class PongState {
    @PrimaryKey var id : Long = 1
    var p1paddle_pos = 0f;
    var p2paddle_pos = 0f;
    var ballx = 0f;
    var bally = 0f;
    var ballvelx = 0f;
    var ballvely = 0f;
    var score1 = 0f;
    var score2 = 0f;

    constructor(){

    }

    constructor(game : PongGame){
        this.p1paddle_pos = game.p1paddle_pos
        this.p2paddle_pos = game.p2paddle_pos
        this.ballx = game.ballx
        this.bally = game.bally
        this.ballvelx = game.ballvelx
        this.ballvely = game.ballvely
        this.score1 = game.score1
        this.score2 = game.score2
    }

    fun applyToGame(game : PongGame){
        game.p1paddle_pos = this.p1paddle_pos
        game.p2paddle_pos = this.p2paddle_pos
        game.ballx = this.ballx
        game.bally = this.bally
        game.ballvelx = this.ballvelx
        game.ballvely = this.ballvely
        game.score1 = this.score1
        game.score2 = this.score2
    }

}