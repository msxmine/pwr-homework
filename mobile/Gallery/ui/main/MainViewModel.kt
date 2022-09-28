package com.example.galeria.ui.main

import android.graphics.BitmapFactory
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import com.example.galeria.Galeria
import com.example.galeria.Image
import com.example.galeria.R
import java.io.File
import java.lang.Math.max

class MainViewModel : ViewModel() {
    val loaded = MutableLiveData<List<Image>>()
    var nextIdx = 1;

    init {
        reload()
    }

    fun reload() {
        var newdata = ArrayList<Image>()
        val caveImage = Image()
        caveImage.rid = "resource/cave.webp"
        caveImage.assetType = 1
        caveImage.resourceID = R.drawable.cave
        caveImage.name = "Jaskinia"
        caveImage.picture = BitmapFactory.decodeResource(Galeria.getAppContext().resources, R.drawable.cave)
        caveImage.rating = 4
        newdata.add(caveImage)

        val landImage = Image()
        landImage.rid = "resource/landscape.webp"
        landImage.assetType = 1
        landImage.resourceID = R.drawable.landscape
        landImage.name = "Krajobraz"
        landImage.picture = BitmapFactory.decodeResource(Galeria.getAppContext().resources, R.drawable.landscape)
        landImage.rating = 5
        newdata.add(landImage)

        var checkedFile = File(Galeria.getAppContext().filesDir, nextIdx.toString() + ".jpg")
        while (checkedFile.exists()){
            var newImage = Image()
            newImage.rid = nextIdx.toString()
            newImage.assetType = 2
            newImage.filePath = checkedFile.path
            newImage.name = "Zdjęcie"
            newImage.picture = BitmapFactory.decodeFile(checkedFile.path)
            newImage.rating =  5
            newdata.add(newImage)
            nextIdx++
            checkedFile = File(Galeria.getAppContext().filesDir, nextIdx.toString() + ".jpg")
        }

        loaded.value = newdata.sortedByDescending { it.rating }
    }

    fun modify(im: Image){
        val curarray = ArrayList(loaded.value)
        val foundidx = curarray.indexOfFirst { it.rid == im.rid }
        curarray[foundidx] = im
        loaded.value = curarray.sortedByDescending { it.rating }

    }

    fun add(fidx: Int){
        var newim = Image()
        var fil = File(Galeria.getAppContext().filesDir, fidx.toString() + ".jpg")
        newim.rid = fidx.toString()
        newim.assetType = 2
        newim.filePath = fil.path
        newim.name = "Zdjęcie"
        newim.picture = BitmapFactory.decodeFile(fil.path)
        newim.rating = 5
        val curarray = ArrayList(loaded.value)
        curarray.add(newim)
        nextIdx = max(nextIdx, fidx+1)
        loaded.value = curarray.sortedByDescending { it.rating }
    }
}