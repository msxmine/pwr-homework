package com.example.todolist

import android.app.Activity
import android.app.AlarmManager
import android.app.Notification
import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import android.os.Bundle
import android.util.Log
import com.google.android.material.floatingactionbutton.FloatingActionButton
import com.google.android.material.snackbar.Snackbar
import androidx.appcompat.app.AppCompatActivity
import android.view.Menu
import android.view.MenuItem
import android.view.View
import android.widget.PopupMenu
import androidx.activity.result.ActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.recyclerview.widget.ItemTouchHelper
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import androidx.room.Room
import com.example.todolist.data.Task
import com.example.todolist.data.TaskDB
import com.example.todolist.data.TaskDao
import kotlinx.coroutines.CoroutineDispatcher
import kotlinx.coroutines.GlobalScope
import kotlinx.coroutines.asCoroutineDispatcher
import kotlinx.coroutines.launch
import java.util.*
import java.util.concurrent.ExecutorService
import java.util.concurrent.Executors
import java.util.concurrent.TimeUnit
import kotlin.collections.ArrayList

class MainActivity : AppCompatActivity() {

    var rvadapter : TasksAdapter = TasksAdapter();
    var myTasks : ArrayList<Task> = ArrayList<Task>()
    var recView : RecyclerView? = null
    var taskdb : TaskDB? = null
    var taskDao : TaskDao? = null
    var dbExecutor : ExecutorService? = null
    val notMap = mutableMapOf<Int, PendingIntent>()

    val taskAddHandler = registerForActivityResult(ActivityResultContracts.StartActivityForResult()) { result: ActivityResult ->
        if (result.resultCode == Activity.RESULT_OK){
            val intent = result.data;
            if (intent != null){
                val newTask = intent.getParcelableExtra<Task>("Task")
                if (intent.getBooleanExtra("Editing", false)){
                    val oldTaskIdx = myTasks.indexOfFirst{ tsk -> tsk.id == newTask!!.id}
                    myTasks = ArrayList(myTasks)
                    myTasks[oldTaskIdx] = newTask!!
                    dbExecutor!!.submit {
                        taskDao!!.updateAll(newTask)
                    }
                    rvadapter.submitList(myTasks)
                    scheduleNotification(newTask.name, newTask.time.time, newTask.id!!)
                }
                else{
                    newTask!!.id = null
                    myTasks = ArrayList(myTasks)
                    dbExecutor!!.submit {
                        val newids = taskDao!!.insertAll(newTask!!)
                        newTask.id = newids[0]
                        GlobalScope.launch {
                            myTasks.add(newTask)
                            rvadapter.submitList(myTasks)
                            scheduleNotification(newTask.name, newTask.time.time, newTask.id!!)
                        }
                    }

                }
            }
        }
    }

    override fun onSaveInstanceState(outState: Bundle) {
        outState?.run {
            putParcelableArrayList("zadania", myTasks)
        }
        super.onSaveInstanceState(outState)
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        taskdb = Room.databaseBuilder(applicationContext, TaskDB::class.java, "maindb").build()
        taskDao = taskdb!!.taskDao()
        if (dbExecutor == null) {
            dbExecutor = Executors.newSingleThreadExecutor()
        }

        if (savedInstanceState != null){
            with(savedInstanceState) {
                myTasks = getParcelableArrayList<Task>("zadania") as ArrayList<Task>
                for (task in myTasks){
                    scheduleNotification(task.name, task.time.time, task.id!!)
                }
            }
        }
        else{
            dbExecutor!!.submit {
                myTasks = ArrayList(taskDao!!.getAll())
                GlobalScope.launch {
                    rvadapter.submitList(myTasks)
                    for (task in myTasks){
                        scheduleNotification(task.name, task.time.time, task.id!!)
                    }
                }
            }
        }

        setContentView(R.layout.activity_main)
        setSupportActionBar(findViewById(R.id.toolbar))


        findViewById<FloatingActionButton>(R.id.fab).setOnClickListener { view ->
            taskAddHandler.launch(Intent(this, AddTaskActivity::class.java))
        }


        recView = findViewById(R.id.rvTaskList)
        recView!!.layoutManager = LinearLayoutManager(this)
        recView!!.adapter = rvadapter

        val swipeHandler = object : SwipeToDeleteCallback(this) {
            override fun onSwiped(viewHolder: RecyclerView.ViewHolder, direction: Int) {
                val oldTasks = ArrayList(myTasks)
                myTasks = ArrayList(myTasks)
                val deletedTask = myTasks[viewHolder.adapterPosition]
                dbExecutor!!.submit {
                    taskDao!!.deleteAll(deletedTask)
                }
                myTasks.removeAt(viewHolder.adapterPosition)
                rvadapter.submitList(myTasks)
                cancelNotification(deletedTask.id!!)

                Snackbar.make(findViewById(R.id.mainView), "Usunięto zadanie", Snackbar.LENGTH_LONG)
                        .setAction("Cofnij", object: View.OnClickListener {
                            override fun onClick(v: View?) {
                                myTasks = oldTasks
                                dbExecutor!!.submit {
                                    taskDao!!.insertAll(deletedTask)
                                }
                                rvadapter.submitList(myTasks)
                                scheduleNotification(deletedTask.name, deletedTask.time.time, deletedTask.id!!)
                            }
                        }).show()

            }
        }
        val itemTouchHelper = ItemTouchHelper(swipeHandler)
        itemTouchHelper.attachToRecyclerView(recView)

        rvadapter.onItemClick = {num ->
            val editInt: Intent = Intent(this, AddTaskActivity::class.java)
            editInt.putExtra("TaskToEdit", myTasks[num])
            taskAddHandler.launch(editInt)
        }

        rvadapter.submitList(myTasks)



    }

    override fun onDestroy() {
        dbExecutor!!.awaitTermination(20, TimeUnit.SECONDS)
        dbExecutor = null
        super.onDestroy()
    }


    fun showSortPopup(v: View){
        val popup = PopupMenu(this, v)
        popup.inflate(R.menu.menu_sort)
        popup.setOnMenuItemClickListener { item ->
            val newlist : ArrayList<Task>

            when (item.itemId){
                R.id.sortTimeItem -> {
                    newlist = ArrayList(myTasks.sortedBy {  it.time})
                }
                R.id.sortPriorityItem -> {
                    newlist = ArrayList(myTasks.sortedByDescending {  it.priority})
                }
                R.id.sortTypeItem -> {
                    newlist = ArrayList(myTasks.sortedBy {  it.image})
                }
                else -> {
                    newlist = ArrayList(myTasks.sortedBy {  it.id})
                }
            }

            myTasks = newlist
            rvadapter.submitList(myTasks)

            true
        }
        popup.show()
    }

    private fun scheduleNotification (taskName: String, time: Long, id: Long){
        val notIntent = Intent(this, NotificationPublisher::class.java)
        notIntent.putExtra("NotificationId", id.toInt())
        notIntent.putExtra("Notification", getNotification(taskName))
        val cbIntent = PendingIntent.getBroadcast(this, id.toInt(), notIntent, PendingIntent.FLAG_UPDATE_CURRENT)
        val alarmMan = getSystemService(Context.ALARM_SERVICE) as AlarmManager
        notMap.put(id.toInt(), cbIntent)
        if (time > System.currentTimeMillis()) {
            alarmMan.setExact(AlarmManager.RTC_WAKEUP, time, cbIntent)
        }
    }

    private fun cancelNotification(id: Long){
        val alarmMan = getSystemService(Context.ALARM_SERVICE) as AlarmManager
        val notInt = notMap.get(id.toInt())
        alarmMan.cancel(notInt)
    }

    private fun getNotification(taskName : String) : Notification {
        val builder = Notification.Builder(this, "default")
        builder.setContentTitle("Zadanie")
        builder.setContentText(taskName)
        builder.setSmallIcon(R.drawable.ic_launcher_foreground)
        builder.setAutoCancel(true)
        builder.setChannelId("default")
        return builder.build()
    }



}