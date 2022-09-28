package com.example.todolist.data

import androidx.room.Database
import androidx.room.RoomDatabase
import androidx.room.TypeConverters

@Database(entities = arrayOf(Task::class), version = 1)
@TypeConverters(DataConverters::class)
abstract class TaskDB : RoomDatabase() {
    abstract fun taskDao(): TaskDao
}