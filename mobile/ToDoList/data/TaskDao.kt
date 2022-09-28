package com.example.todolist.data

import androidx.room.*

@Dao
interface TaskDao {
    @Query("SELECT * FROM task")
    fun getAll(): List<Task>

    @Insert
    fun insertAll(vararg tasks: Task): List<Long>

    @Update
    fun updateAll(vararg tasks: Task)

    @Delete
    fun deleteAll(vararg tasks: Task)
}