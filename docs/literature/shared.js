
function setLang(value){document.body.dataset.lang=value;try{localStorage.setItem('hems-literature-language',value)}catch(e){}}
document.getElementById('language').addEventListener('change',e=>setLang(e.target.value));
try{const v=localStorage.getItem('hems-literature-language');if(['en','fa','both'].includes(v)){setLang(v);document.getElementById('language').value=v}}catch(e){}
