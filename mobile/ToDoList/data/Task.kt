package com.example.todolist.data

import android.os.Parcel
import android.os.Parcelable
import androidx.annotation.DrawableRes
import androidx.room.Entity
import androidx.room.PrimaryKey
import java.util.Date

@Entity
class Task : Parcelable{

        companion object {
                @JvmField
                val CREATOR = object : Parcelable.Creator<Task> {
                        override fun createFromParcel(parcel: Parcel) = Task(parcel)
                        override fun newArray(size: Int) = arrayOfNulls<Task>(size)
                }
        }

        @PrimaryKey(autoGenerate = true) var id : Long?
        var name: String
        @DrawableRes
        var image: Int
        var time: Date
        var priority: Int

        constructor(name: String, image: Int, time: Date, priority: Int){
                this.id = null
                this.name = name
                this.image = image
                this.time = time
                this.priority = priority
        }

        private constructor(parcel: Parcel){
                this.id = parcel.readLong()
                if (this.id == 0L){
                        this.id = null
                }
                this.name = parcel.readString()!!
                this.image = parcel.readInt()
                this.time = Date(parcel.readLong())
                this.priority = parcel.readInt()
        }

        override fun writeToParcel(parcel: Parcel, flags: Int) {
                if (id == null) {
                        parcel.writeLong(0)
                }
                else{
                        parcel.writeLong(id!!)
                }
                parcel.writeString(name)
                parcel.writeInt(image)
                parcel.writeLong(time.time)
                parcel.writeInt(priority)
        }

        override fun describeContents() = 0
}