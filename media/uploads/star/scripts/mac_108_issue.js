	document.addEventListener( "DOMContentLoaded", function() {
	var nav = navigator.userAgent;
	if( nav.indexOf( '10_8') > 0 || nav.indexOf( '10.8') > 0 ) { // we are on lion!
		var qa = document.getElementsByClassName('body');
		if(qa && qa.length > 0 )
		{
			var q = qa[0];
			var text = "<div style='width:100%;height:15pt;border:1px solid black;padding:5px;margin:5px;background-color:#e0e0e0;border-radius:9px;text-align:center;font-size:15pt'>If you encounter difficulties starting a STAR tool on a <span style='font-size:18pt'>Mac</span>, then please read <a href='MacDeveloper.html'>this page</a>.</div>";
			var w = document.createElement("div");
			w.innerHTML = text;
			q.insertBefore(w,q.firstChild);
		}
	}
  });
