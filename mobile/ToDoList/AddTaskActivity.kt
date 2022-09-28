package com.example.todolist

import android.app.Activity
import android.app.DatePickerDialog
import android.app.TimePickerDialog
import android.content.Intent
import android.icu.text.SimpleDateFormat
import android.icu.util.Calendar
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.text.Editable
import android.text.TextWatcher
import android.view.Menu
import android.view.MenuItem
import android.view.View
import android.widget.*
import androidx.annotation.DrawableRes
import com.example.todolist.data.Task
import java.util.*

class AddTaskActivity : AppCompatActivity() {
    var viewedTask: Task? = null;


    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_add_task)
        setSupportActionBar(findViewById(R.id.addTaskToolbar))

        val taskOpText = findViewById<TextView>(R.id.taskOpName)
        val nameField = findViewById<EditText>(R.id.taskNameEntry)
        val dateField = findViewById<EditText>(R.id.taskDateEntry)
        val timeField = findViewById<EditText>(R.id.taskTimeEntry)
        val priorityField = findViewById<SeekBar>(R.id.taskPriorityEntry)
        val myCalendar = Calendar.getInstance()
        val strconvDate = SimpleDateFormat("yyyy-MM-dd")
        val strconvTime = SimpleDateFormat("HH:mm")
        val typeField = findViewById<RadioGroup>(R.id.taskTypeSelector)
        val typeIcons = arrayListOf<Int>(R.drawable.ic_baseline_school_24, R.drawable.ic_baseline_home_work_24, R.drawable.ic_baseline_work_24)
        val typeButtons = arrayListOf<Int>(R.id.taskTypeSchool, R.id.taskTypeHome, R.id.taskTypeJob)
        val taskSaveButton = findViewById<Button>(R.id.taskSaveButton)

        var editing = false
        if (intent.getParcelableExtra<Task>("TaskToEdit") != null) {
            editing = true
            viewedTask = intent.getParcelableExtra<Task>("TaskToEdit")
            taskOpText.text = "Edytuj zadanie"
        }
        else {
            viewedTask = Task("Zadanie", R.drawable.ic_baseline_school_24, Date(), 1)
            taskOpText.text = "Nowe zadanie"
        }

        nameField.setText(viewedTask!!.name)
        myCalendar.time = viewedTask!!.time
        dateField.setText(strconvDate.format(myCalendar.time))
        timeField.setText(strconvTime.format(myCalendar.time))
        priorityField.progress = viewedTask!!.priority
        typeField.clearCheck()
        findViewById<RadioButton>(typeButtons[typeIcons.indexOfFirst { el -> el == viewedTask!!.image }]).isChecked = true



        nameField.addTextChangedListener(object : TextWatcher {
            override fun afterTextChanged(s: Editable?) {
                viewedTask!!.name = nameField.text.toString()
            }

            override fun beforeTextChanged(s: CharSequence?, start: Int, count: Int, after: Int) {
            }
            override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) {
            }
        })

        val datePickerOnDataSetListener = DatePickerDialog.OnDateSetListener { _, year, monthOfYear, dayOfMonth ->
            myCalendar.set(Calendar.YEAR, year)
            myCalendar.set(Calendar.MONTH, monthOfYear)
            myCalendar.set(Calendar.DAY_OF_MONTH, dayOfMonth)
            dateField.setText(strconvDate.format(myCalendar.time))
            viewedTask!!.time = myCalendar.time
        }
        dateField.setOnClickListener {
            DatePickerDialog(this,datePickerOnDataSetListener, myCalendar.get(Calendar.YEAR), myCalendar.get(Calendar.MONTH), myCalendar.get(Calendar.DAY_OF_MONTH)).run {
                show()
            }
        }

        val timePickerOnDataSetListener = TimePickerDialog.OnTimeSetListener {_, hourOfDay, minute ->
            myCalendar.set(Calendar.HOUR_OF_DAY, hourOfDay)
            myCalendar.set(Calendar.MINUTE, minute)
            timeField.setText(strconvTime.format(myCalendar.time))
            viewedTask!!.time = myCalendar.time
        }
        timeField.setOnClickListener {
            TimePickerDialog(this, timePickerOnDataSetListener, myCalendar.get(Calendar.HOUR_OF_DAY), myCalendar.get(Calendar.MINUTE), true).run {
                show()
            }
        }

        priorityField.setOnSeekBarChangeListener( object : SeekBar.OnSeekBarChangeListener {
            override fun onProgressChanged(seekBar: SeekBar?, progress: Int, fromUser: Boolean) {
                viewedTask!!.priority = progress
            }

            override fun onStartTrackingTouch(seekBar: SeekBar?) {}
            override fun onStopTrackingTouch(seekBar: SeekBar?) {}
        })

        fun radioCallback(view: View) {
            if (view is RadioButton){
                if (view.isChecked){
                    when (view.getId()) {
                        R.id.taskTypeSchool ->
                            viewedTask!!.image = R.drawable.ic_baseline_school_24
                        R.id.taskTypeHome ->
                            viewedTask!!.image = R.drawable.ic_baseline_home_work_24
                        R.id.taskTypeJob ->
                            viewedTask!!.image = R.drawable.ic_baseline_work_24
                    }
                }
            }
        }

        findViewById<RadioButton>(R.id.taskTypeSchool).setOnClickListener { radioCallback(it) }
        findViewById<RadioButton>(R.id.taskTypeHome).setOnClickListener { radioCallback(it) }
        findViewById<RadioButton>(R.id.taskTypeJob).setOnClickListener { radioCallback(it) }

        taskSaveButton.setOnClickListener {
            var resultIntent = Intent()
            resultIntent.putExtra("Task", viewedTask)
            resultIntent.putExtra("Editing", editing)
            setResult(Activity.RESULT_OK, resultIntent)
            finish()
        }

    }

    override fun onCreateOptionsMenu(menu: Menu): Boolean {
        menuInflater.inflate(R.menu.menu_addtask, menu)
        return true
    }

    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        setResult(Activity.RESULT_CANCELED)
        finish()
        return true
    }
}