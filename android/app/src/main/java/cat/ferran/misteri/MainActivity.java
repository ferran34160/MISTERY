package cat.ferran.misteri;

import android.app.Activity;
import android.graphics.Color;
import android.os.Bundle;
import android.speech.tts.TextToSpeech;
import android.webkit.JavascriptInterface;
import java.util.Locale;
import android.view.View;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

/** Obre la pàgina del joc (index.html, a assets/) dins d'un WebView a pantalla completa. */
public class MainActivity extends Activity {
    private WebView web;
    private TextToSpeech tts;
    private boolean ttsOk = false;
    private String pendent = null;

    /** Pont cap al sintetitzador de veu d'Android (el WebView no sempre té speechSynthesis). */
    public class Veu {
        @JavascriptInterface
        public void diu(String text, String llengua) {
            runOnUiThread(() -> {
                if (tts == null) return;
                if (!ttsOk) { pendent = text; return; }
                tts.setLanguage(Locale.forLanguageTag(llengua));
                tts.setSpeechRate(0.85f);
                tts.speak(text, TextToSpeech.QUEUE_FLUSH, null, "pista");
            });
        }
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        getWindow().setStatusBarColor(Color.parseColor("#F4ECDF"));
        getWindow().getDecorView().setSystemUiVisibility(View.SYSTEM_UI_FLAG_LIGHT_STATUS_BAR);
        web = new WebView(this);
        web.setBackgroundColor(Color.parseColor("#F4ECDF"));
        setContentView(web);
        WebSettings s = web.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);   // localStorage: progrés, temps i sobrenom
        s.setAllowFileAccess(true);
        tts = new TextToSpeech(this, status -> {
            ttsOk = status == TextToSpeech.SUCCESS;
            if (ttsOk && pendent != null) { String p = pendent; pendent = null; tts.setLanguage(Locale.FRENCH); tts.speak(p, TextToSpeech.QUEUE_FLUSH, null, "pista"); }
        });
        web.addJavascriptInterface(new Veu(), "Veu");
        web.setWebViewClient(new WebViewClient());
        web.setWebChromeClient(new WebChromeClient());   // perquè funcionin confirm() i prompt() de la pàgina
        web.loadUrl("file:///android_asset/index.html");
    }

    @Override
    protected void onDestroy() {
        if (tts != null) { tts.stop(); tts.shutdown(); }
        super.onDestroy();
    }

    /** El botó «enrere» tanca finestres, torna a la llista de casos i, des de la llista, surt. */
    @Override
    public void onBackPressed() {
        web.evaluateJavascript(
            "(function(){var m=document.getElementById('modal');"
            + "if(m&&!m.classList.contains('hidden')){closeModal();return 'm'}"
            + "var b=document.getElementById('back');"
            + "if(b&&!b.classList.contains('hidden')){home();return 'h'}return 'x'})()",
            v -> { if (v != null && v.contains("x")) finish(); });
    }
}
