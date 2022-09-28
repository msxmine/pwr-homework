package com.example.galeria

import androidx.fragment.app.Fragment
import androidx.viewpager2.adapter.FragmentStateAdapter
import com.example.galeria.ui.main.DetailFragment
import com.example.galeria.ui.main.MainFragment

class TabAdapter(fragment: Fragment) : FragmentStateAdapter(fragment) {

    override fun getItemCount(): Int = 2

    override fun createFragment(position: Int): Fragment {
        if (position == 0){
            return MainFragment()
        }
        else{
            return DetailFragment()
        }
    }
}