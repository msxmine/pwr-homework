package com.example.galeria

import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.os.Parcel
import android.os.Parcelable

data class Image(
    var rid : String = "",
    var picture : Bitmap? = null,
    var name : String = "",
    var rating : Int = 0,
    var assetType: Int = 0,
    var resourceID: Int = 0,
    var filePath: String = ""
) : Parcelable{


    constructor(parcel: Parcel) : this() {
        rid = parcel.readString()!!
        assetType = parcel.readInt()!!
        if (assetType == 1){
            resourceID = parcel.readInt()
            picture =  BitmapFactory.decodeResource(Galeria.getAppContext().resources, resourceID)
        }
        if (assetType == 2){
            filePath = parcel.readString()!!
            picture = BitmapFactory.decodeFile(filePath)
        }
        name = parcel.readString()!!
        rating = parcel.readInt()
    }

    override fun writeToParcel(parcel: Parcel, flags: Int) {
        parcel.writeString(rid)
        parcel.writeInt(assetType)
        if (assetType == 1){
            parcel.writeInt(resourceID)
        }
        if (assetType == 2){
            parcel.writeString(filePath)
        }
        parcel.writeString(name)
        parcel.writeInt(rating)
    }

    override fun describeContents() = 0
    companion object CREATOR : Parcelable.Creator<Image> {
        override fun createFromParcel(parcel: Parcel) = Image(parcel)
        override fun newArray(size: Int) = arrayOfNulls<Image>(size)
    }
}