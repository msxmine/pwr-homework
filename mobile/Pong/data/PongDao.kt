package com.example.pong.data

import androidx.room.*
@Dao
interface PongDao {
    @Query("SELECT * FROM pongstate WHERE id = :given")
    fun getAll(given : Long): PongState

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    fun insertAll(vararg tasks: PongState)

    @Update
    fun updateAll(vararg tasks: PongState)

    @Delete
    fun deleteAll(vararg tasks: PongState)
}