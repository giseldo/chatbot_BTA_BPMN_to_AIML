

function IsIE8Browser() {
    var rv = -1;
    var ua = navigator.userAgent;
    var re = new RegExp("Trident\/([0-9]{1,}[\.0-9]{0,})");
    if (re.exec(ua) != null) {
        rv = parseFloat(RegExp.$1);
    }
    return (rv == 4);
    //return true;
}

if (IsIE8Browser()) {
    
    var htmlObj = document.getElementsByTagName('html')[0];
        htmlObj.className = htmlObj.className + ' no-js lt-ie9';

    var element = document.getElementById('biz-ex-support');
    if(Bizagi.App.Model.texts){
        element.innerHTML = Bizagi.AppModel.texts['unsupported'];
    }else{
        element.innerHTML = 'unsupported';
    }
}