var hmContextIds = new Array();
function hmGetContextId(query) {
    var urlParams;
    var match,
        pl = /\+/g,
        search = /([^&=]+)=?([^&]*)/g,
        decode = function (s) { return decodeURIComponent(s.replace(pl, " ")); },
    params = {};
    while (match = search.exec(query))
       params[decode(match[1])] = decode(match[2]);
    if (params["contextid"]) return decodeURIComponent(hmContextIds[params["contextid"]]);
    else return "";
}

hmContextIds["30"]="cogo_docs_top.html";
hmContextIds["18"]="cogo_top.html";
hmContextIds["19"]="cogo_getstarted.html";
hmContextIds["36"]="cogo_preferences_top.html";
hmContextIds["20"]="cogo_projects_top.html";
hmContextIds["37"]="cogo_filetreenav.html";
hmContextIds["39"]="cogo_search_top.html";
hmContextIds["38"]="cogo_output_top.html";
hmContextIds["32"]="cogo_texteditor_top.html";
hmContextIds["33"]="cogo_layouteditor_top.html";
hmContextIds["34"]="cogo_build_top.html";
hmContextIds["35"]="cogo_debugger_top.html";
hmContextIds["13"]="java_top.html";
hmContextIds["24"]="java_keywords.html";
hmContextIds["22"]="kotlin_top.html";
hmContextIds["25"]="kotlin_keywords.html";
hmContextIds["23"]="gradle_top.html";
hmContextIds["40"]="gradle_build.html";
hmContextIds["41"]="using-kotlin-script.html";
hmContextIds["42"]="using-groovy.html";
hmContextIds["10"]="android_applifecycle.html";
hmContextIds["29"]="android_handleconfig.html";
hmContextIds["21"]="android_uicomponents.html";
hmContextIds["27"]="whatever.html";
