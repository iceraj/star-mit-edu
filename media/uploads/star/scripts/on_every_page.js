(function() {
/*
var social_networks = {};
var count = 4 ;

function record_login_status( slot , network, status )
{
	try {
	social_networks = social_networks || {} ;
	social_networks[network] = status ? "Y" : "N" ;
	_gaq.push(["_setCustomVar",slot, network + "_State" , status ? "logged In" : "Not logged in"]);
	if( Object.keys(social_networks).length == count)
	{
		var keys = Object.keys(social_networks)
		keys.sort();
		var event = '' ;
		for( var i = 0 ; i < keys.length ; i++ )
		{
			event = event + ' ' + keys[i] + ':' + social_networks[keys[i]];
		}
		_gaq.push(["_trackEvent","Social_networks", event , location.pathname , true ]) ;
	}
	} finally {}
}
window.record_login_status = record_login_status;
*/
function insert(str) {
	try {
	var q = document.createElement('div');
	q.innerHTML = str;
	document.body.appendChild(q);
	} finally {}
}

function insertScript(src, body) {
	try {
	var q = document.createElement('script');
	q.src = src;
	var w = document.createElement('script');
	w.innerHTML = body;
	document.head.appendChild(q);
	q.onload = function() {
	document.head.appendChild(w);
	}
	
	} finally {}
}
/*
var google_str = '<img style="display:none;" onload="record_login_status(1, \'Google\', true)" onerror="record_login_status(1, \'Google\', false)" src="https://accounts.google.com/CheckCookie?continue=https://www.google.com/intl/en/images/logos/accounts_logo.png">';
var google_plus_str = '<img style="display:none;" onload="record_login_status(2, \'GooglePlus\', true)" onerror="record_login_status(2, \'GooglePlus\', false)" src="https://plus.google.com/up/?continue=https://www.google.com/intl/en/images/logos/accounts_logo.png&amp;type=st&amp;gpsrc=ogpy0">';
var twitter_str = '<img style="display:none;" src="https://twitter.com/login?redirect_after_login=%2Fimages%2Fspinner.gif" onload="record_login_status(3, \'Twitter\', true)" onerror="record_login_status(3, \'Twitter\', false)">';

insert(google_str);
insert(google_plus_str);
insert(twitter_str);

insert("<div id='fb-root' class='fb_reset'></div>");
	window.fbAsyncInit = function(){
		FB.init({ appId:'114924368523313', status:true,  cookie:true, xfbml:true});
		FB.getLoginStatus(function(response){
			if (response.status != "unknown")
			{
				record_login_status(4, "Facebook", true);
			}else{
				record_login_status(4, "Facebook", false);
			}
		});
	};
	// Load the SDK Asynchronously
	(function(d){
		var js, id = 'facebook-jssdk'; if (d.getElementById(id)) {return;}
		js = d.createElement('script'); js.id = id; js.async = true;
		js.src = "//connect.facebook.net/en_US/all.js";
		d.getElementsByTagName('head')[0].appendChild(js);
	}(document));
*/
insertScript( '//cdn.ravenjs.com/1.1.2/jquery,native/raven.min.js',"Raven.config('https://b59437b381614d719bef3eeb7fe91e3b@app.getsentry.com/16929', { whitelistUrls: [/mit\.edu/] }).install();");

})();
