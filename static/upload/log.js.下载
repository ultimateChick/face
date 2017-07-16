(function () {
    var server = window.location.protocol + '//' + window.location.host;

	var vendor = /.*\&(.*)/.exec(window.name)[1];
        
	var srcDesktop = server + '/yws/mapi/ilogrpt?method=putwcplog&chrome_clipper=downloadclient&vendor=' + vendor;

    var srcMobile = server + '/yws/mapi/ilogrpt?method=putwcplog&chrome_clipper=downloadmobile&vendor=' + vendor;

    var srcAd = server + '/yws/mapi/ilogrpt?method=putwcplog&chrome_clipper=gohome&vendor=' + vendor;
    
	var desktopBtn = document.getElementById('desktop');
    
    var mobileBtn = document.getElementById('mobile');
    
    var href = server + '?vendor=' + vendor;
    
    function adLogEntry() {
        logEntry(srcAd);
    }

    function logEntry(src){

	    var i = new Image();

	    i.src = src;
 
 	    return true;
	 };
    
    
     if (desktopBtn) {
        desktopBtn.onclick = function () {
            logEntry(srcDesktop);
        };

        mobileBtn.onclick = function () {
            logEntry(srcMobile);
            mobileBtn.setAttribute('href', href);
        };
     }
    window.vendor = vendor;
    window.adLogEntry = adLogEntry;
    document.forms['_YNoteInfoForm'].action += ("&vendor=" + vendor);
})();