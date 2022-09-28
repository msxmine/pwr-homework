package com.example.galeria

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import android.widget.RatingBar
import android.widget.TextView
import androidx.recyclerview.widget.DiffUtil
import androidx.recyclerview.widget.ListAdapter
import androidx.recyclerview.widget.RecyclerView

class ImageAdapter() : ListAdapter<Image, ImageAdapter.ImageViewHolder>(ImageDiffCallback){

    var onItemClick : ((Int) -> Unit)? = null

    inner class ImageViewHolder(itemView : View) : RecyclerView.ViewHolder(itemView) {
        private  val imagePictureView = itemView.findViewById<ImageView>(R.id.list_image_picture)
        private val imageNameView = itemView.findViewById<TextView>(R.id.list_image_name)
        private val imageRatingView = itemView.findViewById<RatingBar>(R.id.list_image_rating)

        init {
            imageRatingView.setIsIndicator(true)
            itemView.setOnClickListener {
                if (onItemClick != null){
                    onItemClick!!.invoke(adapterPosition)
                }
            }
        }

        fun bind(bound : Image){
            imagePictureView.setImageBitmap(bound.picture)
            imageNameView.setText(bound.name)
            imageRatingView.rating = bound.rating.toFloat()
        }
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ImageViewHolder {
        val view = LayoutInflater.from(parent.context).inflate(R.layout.image_entry, parent, false)
        return ImageViewHolder(view)
    }

    override fun onBindViewHolder(holder: ImageViewHolder, position: Int) {
        val image = getItem(position)
        holder.bind(image)
    }
}

object ImageDiffCallback : DiffUtil.ItemCallback<Image>() {
    override fun areItemsTheSame(oldItem: Image, newItem: Image): Boolean {
        return oldItem == newItem
    }

    override fun areContentsTheSame(oldItem: Image, newItem: Image): Boolean {
        return (oldItem.name == newItem.name && oldItem.rating == newItem.rating)
    }
}