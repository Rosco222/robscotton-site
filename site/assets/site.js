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

  // Twinkling stars (Russell counting stars). Bias the stars into the sky, away from Russell.
  field('.twinkle',84,function(b,i){
    var big=i%6===0;
    b.className=big?'tw big':'tw';
    b.style.setProperty('--s',(big?6+Math.random()*5:2+Math.random()*3)+'px');
    var x,y;do{x=3+Math.random()*94;y=2+Math.pow(Math.random(),1.4)*68;}while(x>60&&x<82&&y>20); // keep clear of Russell
    b.style.setProperty('--x',x+'%');
    b.style.setProperty('--y',y+'%');
    b.style.setProperty('--d',(2+Math.random()*3.5)+'s');
    b.style.setProperty('--delay',(-Math.random()*6)+'s');
  });

  // Shooting stars: six paths across the sky, fired in random order, 2 to 6 seconds apart
  (function(){
    var hosts=document.querySelectorAll('.twinkle');
    if(!hosts.length||!Element.prototype.animate) return;
    if(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    // [start x, start y, end x, end y] as fractions of the header; all stay in the sky
    var PATHS=[[.80,.07,.60,.30],[.97,.05,.84,.22],[.56,.04,.40,.22],[.62,.10,.86,.19],[.99,.20,.86,.44],[.32,.03,.12,.17]];
    hosts.forEach(function(host){
      var last=-1,timer=null,visible=true;
      function shoot(){
        if(!visible||document.hidden){timer=setTimeout(shoot,1500);return;}
        var k;do{k=Math.floor(Math.random()*PATHS.length);}while(k===last);last=k;
        var p=PATHS[k],W=host.clientWidth,H=host.clientHeight;
        var x0=p[0]*W,y0=p[1]*H,dx=(p[2]-p[0])*W,dy=(p[3]-p[1])*H;
        var ang=Math.atan2(dy,dx)*180/Math.PI,len=90+Math.random()*80,dur=650+Math.random()*500;
        var s=document.createElement('i');s.className='shoot';
        s.style.width=len+'px';s.style.left=(x0-len)+'px';s.style.top=y0+'px';
        host.appendChild(s);
        var r='rotate('+ang+'deg)';
        var an=s.animate([
          {opacity:0,transform:'translate(0,0) '+r+' scaleX(.2)'},
          {opacity:1,transform:'translate('+dx*.2+'px,'+dy*.2+'px) '+r+' scaleX(1)',offset:.2},
          {opacity:0,transform:'translate('+dx+'px,'+dy+'px) '+r+' scaleX(.6)'}
        ],{duration:dur,easing:'cubic-bezier(.3,.1,.6,1)'});
        an.onfinish=function(){s.remove();timer=setTimeout(shoot,2000+Math.random()*4000);};
      }
      if('IntersectionObserver' in window){new IntersectionObserver(function(es){visible=es[0].isIntersecting;}).observe(host);}
      timer=setTimeout(shoot,1200+Math.random()*1500);
    });
  })();

  // Russell page drawers: effect layers pinned to the painting, plus sparks, lantern glow and counting
  (function(){
    var layers=document.querySelectorAll('.fx[data-fx]');
    if(!layers.length) return;
    var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
    function fit(fx){
      var host=fx.parentNode,img=host.querySelector('.bg img');
      if(!img||!img.naturalWidth) return;
      var hb=host.getBoundingClientRect(),ib=img.getBoundingClientRect();
      var W=ib.width,H=ib.height,ar=img.naturalWidth/img.naturalHeight;
      var sc=Math.max(W/ar,H),rw=ar*sc,rh=sc;
      var op=getComputedStyle(img).objectPosition.split(' ');
      var ox=parseFloat(op[0])/100,oy=parseFloat(op[1]||'50')/100;
      fx.style.left=(ib.left-hb.left+(W-rw)*(isNaN(ox)?.5:ox))+'px';fx.style.top=(ib.top-hb.top+(H-rh)*(isNaN(oy)?.5:oy))+'px';
      fx.style.width=rw+'px';fx.style.height=rh+'px';
      fx.style.setProperty('--gx',fx.dataset.x+'%');fx.style.setProperty('--gy',fx.dataset.y+'%');
    }
    function fitAll(){layers.forEach(fit);}
    layers.forEach(function(fx){
      var img=fx.parentNode.querySelector('.bg img');
      if(img){ if(img.complete) fit(fx); img.addEventListener('load',function(){fit(fx);}); }
    });
    var rt;window.addEventListener('resize',function(){clearTimeout(rt);rt=setTimeout(fitAll,120);});
    if(reduce||!Element.prototype.animate) return;

    function whenVisible(el,cb){
      var on=false;
      if('IntersectionObserver' in window) new IntersectionObserver(function(es){on=es[0].isIntersecting;cb(on);}).observe(el); else cb(true);
    }
    layers.forEach(function(fx){
      var kind=fx.dataset.fx,timer=null;
      if(kind==='sparks'){
        var live=0;
        function spark(n){
          for(var i=0;i<n&&live<70;i++){
            var s=document.createElement('i');s.className='spark';
            var sz=1.5+Math.random()*2.5;s.style.setProperty('--s',sz+'px');
            s.style.left=fx.dataset.x+'%';s.style.top=fx.dataset.y+'%';
            fx.appendChild(s);live++;
            var unit=fx.clientWidth/1000; // scale the throw with the picture
            var ang=(-170+Math.random()*160)*Math.PI/180,v=(120+Math.random()*260)*unit,g=900*unit,T=.45+Math.random()*.7;
            var kf=[];for(var k=0;k<=4;k++){var t=T*k/4;kf.push({transform:'translate('+(Math.cos(ang)*v*t)+'px,'+(Math.sin(ang)*v*t+.5*g*t*t)+'px) scale('+(1-k*.18)+')',opacity:k===4?0:1});}
            var an=s.animate(kf,{duration:T*1000,easing:'linear'});
            an.onfinish=(function(el){return function(){el.remove();live--;};})(s);
          }
        }
        var tick=0;
        function loop(){ tick++; spark(tick%28===0?16:(Math.random()<.7?2:0)); timer=setTimeout(loop,55); }
        whenVisible(fx.parentNode,function(on){clearTimeout(timer);if(on)loop();});
      }
      if(kind==='count'){
        var n=0;
        function count(){
          n=n%99+1;
          var e=document.createElement('i');e.className='count-n';e.textContent=n;
          var x=parseFloat(fx.dataset.x)+(Math.random()*14-7),y=parseFloat(fx.dataset.y)+(Math.random()*12-6);
          e.style.left=x+'%';e.style.top=y+'%';e.style.fontSize=(fx.clientWidth*(.022+Math.random()*.018))+'px';
          fx.appendChild(e);
          var dx=(Math.random()*80-40)*(fx.clientWidth/1000),dy=-(160+Math.random()*120)*(fx.clientWidth/1000);
          var an=e.animate([{opacity:0,transform:'translate(-50%,-50%) scale(.6)'},{opacity:.95,transform:'translate(calc(-50% + '+dx*.25+'px),calc(-50% + '+dy*.25+'px)) scale(1)',offset:.25},{opacity:0,transform:'translate(calc(-50% + '+dx+'px),calc(-50% + '+dy+'px)) scale(1.1) rotate('+(Math.random()*30-15)+'deg)'}],{duration:3200,easing:'ease-out'});
          an.onfinish=function(){e.remove();};
          timer=setTimeout(count,900+Math.random()*700);
        }
        whenVisible(fx.parentNode,function(on){clearTimeout(timer);if(on)count();});
      }
    });
  })();

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
