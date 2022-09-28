package com.example.galeria

import android.app.Application
import android.content.Context

class Galeria : Application() {
    companion object {
        var ctx : Context? = null
        fun getAppContext() : Context{
            return this.ctx!!
        }
    }

    override fun onCreate() {
        super.onCreate()
        Galeria.ctx = applicationContext
    }
}