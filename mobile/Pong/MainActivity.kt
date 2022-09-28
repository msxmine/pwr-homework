package com.example.pong

import android.annotation.SuppressLint
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import android.view.MotionEvent
import android.widget.Button
import android.widget.TextView
import androidx.room.Room
import com.example.pong.data.PongDB
import com.example.pong.data.PongDao
import com.example.pong.data.PongState
import kotlinx.coroutines.GlobalScope
import kotlinx.coroutines.Job
import kotlinx.coroutines.launch
import java.util.concurrent.CountDownLatch
import java.util.concurrent.Executors
import java.util.concurrent.TimeUnit

class MainActivity : AppCompatActivity() {
    var mg : PongGame = PongGame()

    var glogic : Thread? = null
    @Volatile var finishing = false

    lateinit var statedb : PongDB
    lateinit var statedao : PongDao
    var dbexecutor = Executors.newSingleThreadExecutor()
    val loadedLatch = CountDownLatch(1)

    lateinit var p1scdis : TextView
    lateinit var p2scdis : TextView

    @SuppressLint("ClickableViewAccessibility", "SetTextI18n")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        statedb = Room.databaseBuilder(applicationContext, PongDB::class.java, "maindb").build()
        statedao = statedb.pongDao()

        p1scdis = findViewById<TextView>(R.id.p1text)
        p2scdis = findViewById<TextView>(R.id.p2text)

        dbexecutor.submit{
            val loaded = statedao.getAll(1)
            if (loaded != null){
                loaded.applyToGame(mg)
            }
            loadedLatch.countDown()
        }

        findViewById<PongSurface>(R.id.pong).game = mg
        findViewById<Button>(R.id.p1_up).setOnTouchListener { _, event ->
            if (event.action == MotionEvent.ACTION_DOWN) { mg.wpressed = true }
            else if (event.action == MotionEvent.ACTION_UP){ mg.wpressed = false }
            true
        }
        findViewById<Button>(R.id.p1_down).setOnTouchListener { _, event ->
            if (event.action == MotionEvent.ACTION_DOWN) { mg.spressed = true }
            else if (event.action == MotionEvent.ACTION_UP){ mg.spressed = false }
            true
        }
        findViewById<Button>(R.id.p2_up).setOnTouchListener { _, event ->
            if (event.action == MotionEvent.ACTION_DOWN) { mg.uppressed = true }
            else if (event.action == MotionEvent.ACTION_UP){ mg.uppressed = false }
            true
        }
        findViewById<Button>(R.id.p2_down).setOnTouchListener { _, event ->
            if (event.action == MotionEvent.ACTION_DOWN) { mg.downpressed = true }
            else if (event.action == MotionEvent.ACTION_UP){ mg.downpressed = false }
            true
        }

    }

    override fun onPause() {
        finishing = true
        try {
            glogic?.join()
        }
        catch (ex : InterruptedException){

        }
        dbexecutor.submit {
            val tosave = PongState(mg)
            tosave.id = 1
            statedao.insertAll(tosave)
        }
        super.onPause()
    }

    override fun onResume() {
        finishing = false
        glogic = Thread {
            loadedLatch.await()
            var prevupdate = System.nanoTime()
            var prevsc1 = -1
            var prevsc2 = -1
            while (!finishing){
                val curTim = System.nanoTime()
                mg.handleInput(((curTim - prevupdate).toFloat() * 0.000001).toFloat())
                mg.calculateBall(((curTim - prevupdate).toFloat() * 0.000001).toFloat())
                if (prevsc1 != mg.score1.toInt()) {
                    runOnUiThread { p1scdis.text = "P1: " + mg.score1.toInt() }
                    prevsc1 = mg.score1.toInt()
                }
                if (prevsc2 != mg.score2.toInt()) {
                    runOnUiThread {p2scdis.text = "P2: " + mg.score2.toInt()}
                    prevsc2 = mg.score2.toInt()
                }
                prevupdate = curTim
            }
        }
        glogic!!.start()
        super.onResume()
    }

    override fun onDestroy() {
        dbexecutor.shutdown()
        dbexecutor.awaitTermination(20, TimeUnit.SECONDS)
        super.onDestroy()
    }


}