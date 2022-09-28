package com.example.galeria.ui.main

import android.app.Activity
import android.content.Intent
import androidx.lifecycle.ViewModelProvider
import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.activity.result.ActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.fragment.app.activityViewModels
import androidx.lifecycle.Observer
import androidx.lifecycle.ViewModelProviders
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.galeria.*
import com.google.android.material.floatingactionbutton.FloatingActionButton
import com.google.android.material.tabs.TabLayout

class MainFragment : Fragment() {

    var rvadapter : ImageAdapter = ImageAdapter()
    var recView : RecyclerView? = null

    private lateinit var viewModel: MainViewModel

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?,
                              savedInstanceState: Bundle?): View {
        viewModel = ViewModelProvider(requireActivity()).get(MainViewModel::class.java)
        return inflater.inflate(R.layout.main_fragment, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        val detailModel : DetailViewModel by activityViewModels()

        recView = view.findViewById<RecyclerView>(R.id.rvImageList)
        recView!!.layoutManager = LinearLayoutManager(activity)
        recView!!.adapter = rvadapter

        view.findViewById<FloatingActionButton>(R.id.fab).setOnClickListener { view ->
            val camInt = Intent(activity, ViewFinderActivity::class.java)
            camInt.putExtra("Dest", viewModel.nextIdx)
            startPhotoTaker.launch(camInt)
        }

        rvadapter.onItemClick = {
            detailModel.viewedImage.value = viewModel.loaded.value!![it].copy()
            var tl = requireActivity().findViewById<TabLayout>(R.id.tab_layout)
            var tab = tl.getTabAt(1)
            tab!!.select()
        }

        viewModel.loaded.observe(viewLifecycleOwner, Observer <List<Image>> {
            rvadapter.submitList(it.toList())
        })
        rvadapter.submitList(viewModel.loaded.value!!.toList())


    }

    val startPhotoTaker = registerForActivityResult(ActivityResultContracts.StartActivityForResult()) { result: ActivityResult ->
        if (result.resultCode == Activity.RESULT_OK){
            val intent = result.data;
            if (intent != null) {
                val savedIdx = intent.getIntExtra("Result", 0)
                viewModel.add(savedIdx)
            };
        }
    }

}