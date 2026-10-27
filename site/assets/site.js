/* Rob Scotton | Books: shared behaviour */
(function(){
  // Artwork protection: block right-click "Save Image" and dragging on site imagery.
  // Designated downloads (colouring sheets) are plain links and are not affected.
  document.addEventListener('contextmenu',function(e){ if(e.target&&e.target.tagName==='IMG'){e.preventDefault();} });
  document.addEventListener('dragstart',function(e){ if(e.target&&e.target.tagName==='IMG'){e.preventDefault();} });

  // Mobile nav
  var burger=document.querySelector('.burger'),nav=document.querySelector('.nav');
  if(burger&&nav){
    burger.addEventListener('click',function(){
      var open=nav.classList.toggle('open');
      burger.setAttribute('aria-expanded',open?'true':'false');
    });
    nav.querySelectorAll('a').forEach(function(a){a.addEventListener('click',function(){nav.classList.remove('open');burger.setAttribute('aria-expanded','false');});});
  }

  // Scroll-triggered reveals (rocket launch, section reveals)
  var io=('IntersectionObserver' in window)?new IntersectionObserver(function(entries){
    entries.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add('in-view'); io.unobserve(e.target);} });
  },{threshold:.25}):null;
  document.querySelectorAll('.reveal,.launch').forEach(function(el){ io?io.observe(el):el.classList.add('in-view'); });


  // Where-to-buy region toggle (US / UK). Remembers the choice in this browser when it can.
  document.querySelectorAll('.region-toggle').forEach(function(t){
    var sec=t.closest('section');
    function set(r){
      t.querySelectorAll('button').forEach(function(b){b.setAttribute('aria-pressed',b.dataset.set===r?'true':'false');});
      sec.querySelectorAll('.region').forEach(function(el){el.hidden=el.dataset.region!==r;});
      try{localStorage.setItem('rs-region',r);}catch(e){}
    }
    t.addEventListener('click',function(e){var b=e.target.closest('button');if(b)set(b.dataset.set);});
    var saved=null;try{saved=localStorage.getItem('rs-region');}catch(e){}
    if(saved==='uk')set('uk');
  });


  // Splat's rocket adventure in the splatthecat.com section.
  // Seven flights play one after another, each measured from the live layout so they fit any screen:
  //  1 launch from behind the books   2 distant return   3 far, far away   4 loop-the-loop
  //  5 hide-and-seek behind the books 6 dive behind the shelf             7 close whoosh back up
  (function(){
    var sec=document.querySelector('.portal'), rk=sec&&sec.querySelector('.rocket');
    if(!sec||!rk) return;
    var AXIS=26.6;                       // the rocket artwork points 26.6deg above horizontal
    var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
    var G={};                            // live geometry
    function deg(dx,dy){return Math.atan2(dy,dx)*180/Math.PI;}
    function measure(){
      var sr=sec.getBoundingClientRect(), lp=sec.querySelector('.launchpad').getBoundingClientRect();
      var sh=sec.querySelector('.shelf').getBoundingClientRect(), k=sec.querySelector('.kicker').getBoundingClientRect();
      G={W:sec.clientWidth,H:sec.clientHeight,rw:rk.offsetWidth,rh:rk.offsetHeight,
         lpL:lp.left-sr.left,lpT:lp.top-sr.top,lpW:lp.width,lpH:lp.height,
         shT:sh.top-sr.top,shH:sh.height,kT:k.top-sr.top,narrow:sec.clientWidth<861};
      // resting spot for reduced motion
      rk.style.setProperty('--xr',Math.round(G.narrow?G.W*0.5-G.rw*0.45:G.lpL+G.lpW*0.5-G.rw*0.5)+'px');
      rk.style.setProperty('--yr',Math.round(G.lpT+G.lpH*0.5-G.rh*0.5)+'px');
      rk.style.setProperty('--r1','-30deg');
    }
    // A flight is a path of visual-centre points p(t), t in 0..1, plus a scale.
    // Facing follows the path: moving right uses the artwork as drawn, moving left mirrors it,
    // and 'spin' keeps it unmirrored so it can turn right round (for the loop).
    function frames(path,s,opts){
      opts=opts||{}; var n=opts.n||36, out=[], face=null;
      for(var i=0;i<=n;i++){
        var t=i/n, a=path(Math.max(0,t-0.01)), b=path(Math.min(1,t+0.01)), p=path(t);
        var dx=b.x-a.x, dy=b.y-a.y, flip;
        if(opts.spin) flip=false; else { if(face===null) face=dx<0; flip=face; }
        var rot=flip? deg(-dx,dy)+AXIS : deg(dx,dy)+AXIS;
        var x=p.x-G.rw/2, y=p.y-G.rh/2;
        out.push({offset:t,transform:'translate('+x.toFixed(1)+'px,'+y.toFixed(1)+'px) scale('+(flip?-s:s)+','+s+') rotate('+rot.toFixed(1)+'deg)',opacity:opts.op||1});
      }
      return out;
    }
    function line(x0,y0,x1,y1,wob){return function(t){return {x:x0+(x1-x0)*t,y:y0+(y1-y0)*t+(wob?Math.sin(t*Math.PI*wob.n)*wob.a:0)};};}
    function arc(x0,y0,x1,y1,lift){return function(t){return {x:x0+(x1-x0)*t,y:y0+(y1-y0)*t-Math.sin(t*Math.PI)*lift};};}
    function chain(parts){ // [{f,len}] joined in proportion to length
      var tot=parts.reduce(function(a,p){return a+p.len;},0);
      return function(t){var d=t*tot;for(var i=0;i<parts.length;i++){if(d<=parts[i].len||i===parts.length-1)return parts[i].f(Math.min(1,d/parts[i].len));d-=parts[i].len;}};
    }
    function flights(){
      var W=G.W,H=G.H,rw=G.rw,rh=G.rh,n=G.narrow;
      var colX=n? W*0.62 : G.lpL+G.lpW*0.55;           // the open sky to the right of / below the words
      var skyT=n? G.lpT : G.lpT, skyB=n? G.lpT+G.lpH : G.shT;
      var topY=n? G.lpT+G.lpH*0.3 : Math.max(G.kT*0.6, 60);
      var shelfY=G.shT+G.shH*0.42;
      var R=Math.min(G.lpW*0.3,(skyB-skyT)*0.36), cx=colX, cy=skyT+(skyB-skyT)*0.45;
      return [
        // 1 launch: rise from behind the books and climb out top right along the rocket's angle
        {k:frames(line(n?rw*0.1:G.lpL-rw*0.1,H+rh*0.6,W+rw*0.6,n?G.lpT-rh*0.4:-rh*0.5),1),d:5000,e:'cubic-bezier(.5,0,.85,.55)',p:1600},
        // 2 distant return: small, right to left across the top
        {k:frames(line(W+rw*0.3,topY+40,-rw*0.3,topY),n?0.24:0.3,{op:.85}),d:7000,e:'linear',p:1400},
        // 3 far, far away: tiny, left to right in a gentle arc
        {k:frames(arc(-rw*0.2,n?topY+10:topY+55,W+rw*0.2,n?topY+30:topY+75,n?20:30),n?0.11:0.14,{op:.7}),d:8000,e:'linear',p:1200},
        // 4 loop-the-loop in the open sky
        {k:frames(chain([{f:line(cx+R,H+rh*0.4,cx+R,cy),len:H+rh*0.4-cy},
                         {f:function(t){var a=t*Math.PI*2;return {x:cx+R*Math.cos(a),y:cy-R*Math.sin(a)};},len:2*Math.PI*R},
                         {f:line(cx+R,cy,cx+R+rw*0.6,-rh*0.6),len:cy+rh*0.6}]),n?0.4:0.55,{spin:true,n:60}),d:6500,e:'ease-in-out',p:1600},
        // 5 hide-and-seek: bob along behind the book covers, right to left
        {k:frames(line(W+rw*0.3,shelfY,-rw*0.3,shelfY,{n:6,a:n?10:16}),n?0.32:0.4,{n:48}),d:7000,e:'linear',p:1200},
        // 6 dive: swoop in from the top right and disappear behind the bookshelf
        {k:frames(arc(W+rw*0.4,-rh*0.3,n?W*0.3:G.lpL+G.lpW*0.15,H+rh*0.3,-(n?40:90)),n?0.5:0.7),d:3200,e:'cubic-bezier(.55,0,1,.6)',p:900},
        // 7 whoosh: burst back up from behind the books, big and close, and away
        {k:frames(line(colX+rw*0.05,H+rh*1.1,colX+rw*0.45,-rh*1.2),n?0.95:1.25),d:1900,e:'cubic-bezier(.3,0,.6,1)',p:3600}
      ];
    }
    measure();
    if(reduce) return;
    var queue=[], idx=0, cur=null, timer=null, running=false;
    function hide(){rk.style.opacity='0';}
    function next(){
      if(!running) return;
      if(idx===0) queue=flights();
      var f=queue[idx]; idx=(idx+1)%queue.length;
      rk.style.opacity='';
      cur=rk.animate(f.k,{duration:f.d,easing:f.e,fill:'forwards'});
      cur.onfinish=function(){var a=cur;cur=null;hide();if(a)a.cancel();timer=setTimeout(next,f.p);};
    }
    function start(){ if(running) return; running=true; if(cur){cur.play();} else {clearTimeout(timer); next();} }
    function stop(){ running=false; if(cur) cur.pause(); clearTimeout(timer); }
    hide();
    if('IntersectionObserver' in window){
      new IntersectionObserver(function(es){es.forEach(function(e){e.isIntersecting?start():stop();});},{threshold:.2}).observe(sec);
    } else start();
    var img=rk.querySelector('img');
    if(img&&!img.complete) img.addEventListener('load',measure);
    var rt; window.addEventListener('resize',function(){clearTimeout(rt);rt=setTimeout(function(){measure();queue=flights();},150);});
  })();

  // Bubble + snow particle fields
  function field(sel,n,make){
    document.querySelectorAll(sel).forEach(function(host){
      var frag=document.createDocumentFragment();
      for(var i=0;i<n;i++){var b=document.createElement('i');make(b,i);frag.appendChild(b);}
      host.appendChild(frag);
    });
  }
  field('.bubbles',22,function(b){
    var s=8+Math.random()*44;
    b.style.setProperty('--s',s+'px');
    b.style.setProperty('--x',(Math.random()*100)+'%');
    b.style.setProperty('--d',(14+Math.random()*16)+'s');
    b.style.setProperty('--delay',(-Math.random()*30)+'s');
  });
  field('.snow',40,function(b){
    var s=2+Math.random()*5;
    b.style.setProperty('--s',s+'px');
    b.style.setProperty('--x',(Math.random()*100)+'%');
    b.style.setProperty('--d',(9+Math.random()*14)+'s');
    b.style.setProperty('--delay',(-Math.random()*20)+'s');
  });

  // Floating splatthecat.com tab after a little scrolling
  var fl=document.querySelector('.floater');
  if(fl){ var shown=false; window.addEventListener('scroll',function(){ if(!shown&&window.scrollY>420){fl.classList.add('show');shown=true;} },{passive:true}); }

  // Lightbox
  var items=Array.prototype.slice.call(document.querySelectorAll('.zoom'));
  if(items.length){
    var dlg=document.createElement('dialog');dlg.className='lb';
    dlg.innerHTML='<button class="close" aria-label="Close">×</button><button class="nav-btn prev" aria-label="Previous">‹</button><button class="nav-btn next" aria-label="Next">›</button><figure style="margin:0"><img alt=""><figcaption></figcaption></figure>';
    document.body.appendChild(dlg);
    var img=dlg.querySelector('img'),cap=dlg.querySelector('figcaption'),idx=0;
    function show(i){
      idx=(i+items.length)%items.length;
      var el=items[idx];
      img.src=el.getAttribute('data-full')||el.querySelector('img').currentSrc||el.querySelector('img').src;
      img.alt=el.querySelector('img').alt||'';
      cap.textContent=el.getAttribute('data-caption')||'';
      if(!dlg.open)dlg.showModal();
    }
    items.forEach(function(el,i){el.addEventListener('click',function(ev){ev.preventDefault();show(i);});});
    dlg.querySelector('.close').addEventListener('click',function(){dlg.close();});
    dlg.querySelector('.prev').addEventListener('click',function(){show(idx-1);});
    dlg.querySelector('.next').addEventListener('click',function(){show(idx+1);});
    dlg.addEventListener('click',function(e){ if(e.target===dlg)dlg.close(); });
    dlg.addEventListener('keydown',function(e){ if(e.key==='ArrowRight')show(idx+1); if(e.key==='ArrowLeft')show(idx-1); });
    if(items.length<2){dlg.querySelector('.prev').hidden=true;dlg.querySelector('.next').hidden=true;}
  }

  // Audio player
  document.querySelectorAll('.player').forEach(function(p){
    var a=p.querySelector('audio'),btn=p.querySelector('button'),bar=p.querySelector('.bar i'),t=p.querySelector('.time');
    var play='<svg viewBox="0 0 24 24" width="26" height="26" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>';
    var pause='<svg viewBox="0 0 24 24" width="26" height="26" fill="currentColor"><path d="M6 5h4v14H6zm8 0h4v14h-4z"/></svg>';
    btn.innerHTML=play;
    function fmt(s){s=Math.floor(s||0);return Math.floor(s/60)+':'+('0'+(s%60)).slice(-2);}
    btn.addEventListener('click',function(){ if(a.paused){a.play();}else{a.pause();} });
    a.addEventListener('play',function(){btn.innerHTML=pause;btn.setAttribute('aria-label','Pause');});
    a.addEventListener('pause',function(){btn.innerHTML=play;btn.setAttribute('aria-label','Play');});
    a.addEventListener('timeupdate',function(){ if(a.duration){bar.style.width=(a.currentTime/a.duration*100)+'%';t.textContent=fmt(a.currentTime)+' / '+fmt(a.duration);} });
    a.addEventListener('loadedmetadata',function(){t.textContent='0:00 / '+fmt(a.duration);});
    p.querySelector('.bar').addEventListener('click',function(e){ var r=e.currentTarget.getBoundingClientRect(); if(a.duration)a.currentTime=(e.clientX-r.left)/r.width*a.duration; });
  });
})();
