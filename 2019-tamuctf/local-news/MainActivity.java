package com.tamu.ctf.hidden;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.os.Bundle;
import android.support.v4.content.LocalBroadcastManager;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import io.michaelrocks.paranoid.Deobfuscator$app$Debug;

public class MainActivity extends AppCompatActivity {
    /* Access modifiers changed, original: protected */
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView((int) R.layout.activity_main);
        BroadcastReceiver hidden = new BroadcastReceiver() {
            public void onReceive(Context context, Intent intent) {
                Log.d(MainActivity.this.getString(R.string.flag), Deobfuscator$app$Debug.getString(0));
            }
        };
        IntentFilter filter = new IntentFilter();
        filter.addAction(getString(R.string.hidden_action));
        LocalBroadcastManager.getInstance(this).registerReceiver(hidden, filter);
    }
}
