package cat.ferran.misteri;

import android.app.Activity;
import android.graphics.Color;
import android.os.Bundle;
import android.view.View;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

/** Obre la pàgina del joc (index.html, a assets/) dins d'un WebView a pantalla completa. */
public class MainActivity extends Activity {
    private WebView web;

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
        web.setWebViewClient(new WebViewClient());
        web.setWebChromeClient(new WebChromeClient());   // perquè funcionin confirm() i prompt() de la pàgina
        web.loadUrl("file:///android_asset/index.html");
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
