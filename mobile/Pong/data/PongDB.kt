package com.example.pong.data

import androidx.room.Database
import androidx.room.RoomDatabase

@Database(entities = arrayOf(PongState::class), version = 1)
abstract class PongDB : RoomDatabase() {
    abstract fun pongDao(): PongDao
}