
(function(){
  function colors(i){return ['#7c2f2a','#176b63','#b8873a','#345995','#8b5e34','#5d5a8c','#2f6f3e'][i%7];}
  function dashes(i){return [[],[8,4],[2,3],[10,4,2,4],[1,4],[12,3,3,3],[6,3,1,3]][i%7];}
  function points(i){return ['circle','rect','triangle','rectRot','crossRot','star','cross'][i%7];}
  document.querySelectorAll('.md-panel').forEach(function(panel){
    const preview=panel.querySelector('.md-preview'), editor=panel.querySelector('.md-editor');
    const edit=panel.querySelector('.edit-md'), save=panel.querySelector('.save-md'), cancel=panel.querySelector('.cancel-md');
    const key='VNM:'+panel.id; const source=panel.getAttribute('data-md-source'); const stored=localStorage.getItem(key); let original=stored||preview.dataset.markdown||'';
    function render(md){preview.innerHTML=marked.parse(md);}
    render(original); editor.value=original;
    edit.addEventListener('click',function(){preview.classList.add('hidden');editor.classList.remove('hidden');edit.classList.add('hidden');save.classList.remove('hidden');cancel.classList.remove('hidden');});
    save.addEventListener('click',async function(){
      original=editor.value;
      if(source){
        const response = await fetch('/api/save-section',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({source:source,markdown:original})});
        if(!response.ok){alert('Save failed: '+await response.text());return;}
      } else {
        localStorage.setItem(key,original);
      }
      render(original);preview.classList.remove('hidden');editor.classList.add('hidden');edit.classList.remove('hidden');save.classList.add('hidden');cancel.classList.add('hidden');
    });
    cancel.addEventListener('click',function(){editor.value=original;preview.classList.remove('hidden');editor.classList.add('hidden');edit.classList.remove('hidden');save.classList.add('hidden');cancel.classList.add('hidden');});
  });
  function makeChart(canvas, payload, subsetIndex){
    if(!canvas || !window.Chart) return;
    const series = subsetIndex===undefined ? payload.series : [payload.series[subsetIndex]];
    new Chart(canvas.getContext('2d'), {
      type:'line',
      data:{datasets:series.map(function(s,i){return {label:s.label+' ['+s.code+']', data:s.points.map(function(p){return {x:p.year,y:p.value};}), borderColor:colors(subsetIndex===undefined?i:subsetIndex), backgroundColor:colors(subsetIndex===undefined?i:subsetIndex), borderDash:dashes(subsetIndex===undefined?i:subsetIndex), pointStyle:points(subsetIndex===undefined?i:subsetIndex), tension:.25, pointRadius:2, borderWidth:2.4};})},
      options:{responsive:true,maintainAspectRatio:false,interaction:{mode:'index',intersect:false},plugins:{legend:{position:'bottom'},title:{display:subsetIndex!==undefined,text:series[0].label}},scales:{x:{type:'linear',title:{display:true,text:'Year'},ticks:{precision:0}},y:{title:{display:true,text:payload.unit}}}}
    });
  }
  (window.REPORT_CHARTS||[]).forEach(function(payload){
    if(!payload.series || !payload.series.length) return;
    makeChart(document.getElementById(payload.id), payload);
    if(payload.smallMultiples){payload.series.forEach(function(_s,i){makeChart(document.getElementById(payload.id+'-'+i), payload, i);});}
  });
})();

