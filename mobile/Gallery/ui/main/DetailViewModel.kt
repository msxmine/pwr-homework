package com.example.galeria.ui.main

import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import com.example.galeria.Image

class DetailViewModel : ViewModel() {
    var viewedImage = MutableLiveData<Image>()
}