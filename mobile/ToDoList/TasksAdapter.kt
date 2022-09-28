package com.example.todolist

import android.content.res.ColorStateList
import android.graphics.Color
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import android.widget.TextView
import androidx.recyclerview.widget.DiffUtil
import androidx.recyclerview.widget.ListAdapter
import androidx.recyclerview.widget.RecyclerView
import com.example.todolist.data.Task
import java.text.DateFormat
import java.text.SimpleDateFormat

class TasksAdapter() : ListAdapter<Task, TasksAdapter.TaskViewHolder>(TaskDiffCallback) {

    var onItemClick: ((Int) -> Unit)? = null

    inner class TaskViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        private val taskIconView: ImageView = itemView.findViewById(R.id.taskIcon)
        private val taskNameView: TextView = itemView.findViewById(R.id.taskName)
        private val taskDateView: TextView = itemView.findViewById(R.id.taskDate)
        private var currentTask: Task? = null
        private val datForm: DateFormat = SimpleDateFormat("yyyy-MM-dd HH:mm")
        private val colors = arrayListOf<Int>(Color.rgb(0, 181, 0), Color.rgb(255, 255, 0), Color.rgb(255, 0, 0))

        init {
            itemView.setOnLongClickListener {
                if (onItemClick != null) {
                    onItemClick!!.invoke(adapterPosition)
                    return@setOnLongClickListener true
                }
                else{
                    return@setOnLongClickListener false
                }
            }
        }

        fun bind(bound: Task){
            currentTask = bound
            taskIconView.setImageResource(bound.image)
            taskIconView.backgroundTintList = ColorStateList.valueOf(colors[bound.priority])
            taskNameView.text = bound.name
            taskDateView.text = datForm.format(bound.time)
        }


    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): TaskViewHolder {
        val view = LayoutInflater.from(parent.context).inflate(R.layout.task_item, parent, false)
        return TaskViewHolder(view)
    }

    override fun onBindViewHolder(holder: TaskViewHolder, position: Int) {
        val task = getItem(position)
        holder.bind(task)
    }




}

object TaskDiffCallback : DiffUtil.ItemCallback<Task>() {
    override fun areItemsTheSame(oldItem: Task, newItem: Task): Boolean {
        return oldItem == newItem
    }
    override fun areContentsTheSame(oldItem: Task, newItem: Task): Boolean {
        return oldItem.id == newItem.id
    }
}