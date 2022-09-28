package com.example.galeria.ui.main

import android.os.Bundle
import android.text.Editable
import android.text.TextWatcher
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.EditText
import android.widget.ImageView
import android.widget.RatingBar
import androidx.fragment.app.Fragment
import androidx.fragment.app.activityViewModels
import androidx.lifecycle.Observer
import com.example.galeria.Image
import com.example.galeria.R

class DetailFragment : Fragment() {

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        return inflater.inflate(R.layout.detail_fragment, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        val model: DetailViewModel by activityViewModels()
        val mainmod: MainViewModel by activityViewModels()

        val imageView = view.findViewById<ImageView>(R.id.detail_image)
        val nameView = view.findViewById<EditText>(R.id.detail_name)
        val ratingView = view.findViewById<RatingBar>(R.id.detail_rating)
        model.viewedImage.observe(viewLifecycleOwner, Observer <Image> {
                imageView.setImageBitmap(it.picture)
                nameView.setText(it.name)
                ratingView.rating = it.rating.toFloat()
        })

        nameView.addTextChangedListener(object : TextWatcher {
            override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) {}
            override fun beforeTextChanged(s: CharSequence?, start: Int, count: Int, after: Int) {}
            override fun afterTextChanged(s: Editable?) {
                var myim = model.viewedImage.value!!.copy()
                myim.name = s.toString()
                model.viewedImage.value!!.name = s.toString()
                mainmod.modify(myim)
            }
        })
        ratingView.setOnRatingBarChangeListener { ratingBar, rating, fromUser ->
            var myim = model.viewedImage.value!!.copy()
            myim.rating = rating.toInt()
            model.viewedImage.value!!.rating = rating.toInt()
            mainmod.modify(myim)
        }
    }

}