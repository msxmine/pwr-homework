package com.example.todolist

import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent

class NotificationPublisher : BroadcastReceiver() {
    override fun onReceive(context: Context?, intent: Intent?) {
        val notificationMan = context?.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
        val notificationChannel = NotificationChannel("default", "Zadania", NotificationManager.IMPORTANCE_HIGH)
        if (notificationMan != null) {
            notificationMan.createNotificationChannel(notificationChannel)
        }
        val notification = intent?.getParcelableExtra<Notification>("Notification")
        val notificationId = intent?.getIntExtra("NotificationId", 0)
        if (notificationMan != null && notification != null && notificationId != null ) {
            notificationMan.notify(notificationId, notification)
        }
    }
}