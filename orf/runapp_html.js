var x = document.getElementsByClassName('body')[0];
var inner = '' ;
inner += '<div id="app_div" style="overflow: auto; resize: vertical; border: 2px solid black; position: relative; height: 724px; ">';
inner += '<iframe id="app" src="../media/uploads/star/html/orf/app2.html" style="width:99%;height:99%;border:0px;"></iframe>';
x.innerHTML = inner;
x.style.padding = '0px 5px 5px 0px';
