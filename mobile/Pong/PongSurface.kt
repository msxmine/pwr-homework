package com.example.pong

import android.content.Context
import android.graphics.*
import android.util.AttributeSet
import android.view.SurfaceHolder
import android.view.SurfaceView
import android.view.View
import android.view.WindowManager
import androidx.core.content.ContextCompat.getSystemService
import kotlinx.coroutines.GlobalScope
import kotlinx.coroutines.Job
import kotlinx.coroutines.coroutineScope
import kotlinx.coroutines.launch

class PongSurface( ctx : Context, attr : AttributeSet) : SurfaceView(ctx,attr), SurfaceHolder.Callback, Runnable {
    @Volatile
    var drawing = false
    var game : PongGame? = null

    var drawThread : Thread? = null
    var surfaceReady = false
    var padPaint: Paint = Paint()
    var ballPaint: Paint = Paint()

    var frametime_micro = (1000000.0 / context.display!!.refreshRate).toInt()

    init {
        holder.addCallback(this)
        padPaint.style = Paint.Style.FILL
        padPaint.alpha = 255
        padPaint.color = Color.BLACK
        padPaint.xfermode = PorterDuffXfermode(PorterDuff.Mode.CLEAR)
        ballPaint.style = Paint.Style.FILL
        ballPaint.strokeWidth = 3f
        ballPaint.alpha = 255
        ballPaint.color = Color.BLACK
        ballPaint.xfermode = PorterDuffXfermode(PorterDuff.Mode.CLEAR)
    }

    override fun surfaceChanged(holder: SurfaceHolder, format: Int, width: Int, height: Int) {
    }

    override fun surfaceDestroyed(holder: SurfaceHolder) {
        stopDrawThread()
        holder.surface.release()
        surfaceReady = false
    }

    override fun surfaceCreated(holder: SurfaceHolder) {
        if (drawThread != null){
            drawing = false;
            try {
                drawThread!!.join()
            }
            catch (ex : InterruptedException){

            }
        }

        surfaceReady = true
        startDrawThread()
    }

    fun startDrawThread(){
        if (surfaceReady && drawThread == null){
            drawThread = Thread(this, "Drawer");
            drawing = true
            drawThread!!.start()
        }
    }

    fun stopDrawThread(){
        if (drawThread != null){
            drawing = false
            while (true){
                try {
                    drawThread!!.join(5000)
                    break
                }
                catch (e:Exception){

                }
            }
            drawThread = null
        }
    }

    fun convertX(x: Float) : Float{
        return (width.toFloat()/2f)*(1f+x)
    }

    fun convertY(y: Float) : Float{
        return (height.toFloat()/2f)*(1f-y)
    }

    override fun run() {
        var frameStartTime : Long;
        var frameTime : Long;
        try {
            while(drawing){
                if (holder == null){
                    return
                }
                frameStartTime = System.nanoTime()
                val canvas = holder.lockCanvas()
                if (canvas != null){
                    if (game != null) {
                        canvas.drawColor(Color.WHITE)
                        canvas.drawRect(convertX(-1f), convertY(game!!.p1paddle_pos + (game!!.paddle_height/2f)), convertX(-0.99f), convertY(game!!.p1paddle_pos - (game!!.paddle_height/2f)), padPaint)
                        canvas.drawRect(convertX(0.99f), convertY(game!!.p2paddle_pos + (game!!.paddle_height/2f)), convertX(1f), convertY(game!!.p2paddle_pos - (game!!.paddle_height/2f)), padPaint)
                        canvas.drawCircle(convertX(game!!.ballx), convertY(game!!.bally), 10f, ballPaint)
                        holder.unlockCanvasAndPost(canvas)
                    }
                }
            }
        }
        catch(e:Exception){

        }
    }

}