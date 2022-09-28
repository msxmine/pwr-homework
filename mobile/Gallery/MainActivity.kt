package com.example.galeria

import android.app.Activity
import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import androidx.activity.result.ActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.activity.viewModels
import com.example.galeria.ui.main.DetailViewModel
import com.example.galeria.ui.main.MainFragment
import com.example.galeria.ui.main.MainViewModel

class MainActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.main_activity)
        if (savedInstanceState == null) {
            supportFragmentManager.beginTransaction()
                    .replace(R.id.container, TabbedFragment())
                    .commitNow()

            val mainModel: MainViewModel by viewModels()
            val detailModel: DetailViewModel by viewModels()
            detailModel.viewedImage.value = mainModel.loaded.value!![0].copy()
        }

    }

}