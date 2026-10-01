//<![CDATA[
	var platform = navigator.platform;
	platform = platform.toLowerCase();
	if( platform.indexOf( "linux" ) >= 0)
	{
		var href = document.location.href ;
		var ra_index = href.indexOf("runapp.html")
		if(ra_index > 0)
		{
			var base = href.substring(0,ra_index);
			var new_url = base+'download/index.html';
			window.location = new_url;
		}

	}
//]]>
