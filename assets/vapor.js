/* Vending Solutions: slow drifting vapor background (WebGL fbm, CSS fallback). */
(function () {
  var cv = document.getElementById("vapor");
  if (!cv) return;
  var root = document.documentElement;
  var still = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var phone = Math.min(screen.width, screen.height) < 700 || /Mobi|Android/i.test(navigator.userAgent);
  var gl = cv.getContext("webgl", { alpha: false, antialias: false, depth: false, powerPreference: "low-power" });
  if (!gl) { root.classList.add("no-gl"); return; }

  var RIB = phone ? 3 : 5;
  var vs = "attribute vec2 a;void main(){gl_Position=vec4(a,0.,1.);}";
  // Seamless loop: noise is periodic in x and every motion repeats exactly every L seconds,
  // and JS feeds t modulo L, so the drift never resets or cuts.
  var L = 240.0;
  // A few short vapor wisps drifting left -> right (fixed layer, ignores page scroll on purpose). Each one lives in a wrapped x-domain of width W
  // (screen + off-screen run-up) and moves a whole number of W per loop, so the 240 s loop is seamless.
  var fs = [
    "#ifdef GL_FRAGMENT_PRECISION_HIGH\nprecision highp float;\n#else\nprecision mediump float;\n#endif",
    "uniform vec2 r;uniform float t;",
    "const float L=" + L.toFixed(1) + ";const float TAU=6.2831853;",
    "float h(vec2 p){p=fract(p*vec2(.1031,.1030));p+=dot(p,p.yx+33.33);return fract((p.x+p.y)*p.x);}",
    "float n(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);",
    " return mix(mix(h(i),h(i+vec2(1,0)),f.x),mix(h(i+vec2(0,1)),h(i+1.),f.x),f.y);}",
    // x,y in screen units. k = passes per loop, Wr = wrap width (bigger = longer gap before it reappears),
    // LN = length, sl = slope (diagonal drift), cu = curl strength, m = breathing rate (integer -> loops cleanly)
    "float ribbon(float x,float y,float k,float y0,float ph,float sl,float Wr,float LN,float cu,float m){",
    " float tt=TAU*t/L;",
    " float u=mod(x-Wr*k*t/L+ph*.55,Wr);",
    " float env=smoothstep(0.,LN*.5,u)*smoothstep(LN,LN*.7,u);",
    " if(env<=0.)return 0.;",
    " float a=u/LN;",
    " float yc=y0+sl*(x-.5)+.05*sin(u*3.6+ph+tt*2.)+.026*sin(u*7.3-tt*3.+ph*1.7)+.01*sin(u*15.-tt*5.+ph);",
    " float cc=LN*(.35+.25*sin(ph*3.));",                             // a soft eddy somewhere along the wisp
    " yc+=cu*exp(-pow((u-cc)/.12,2.))*sin((u-cc)*26.+tt*3.+ph);",
    " float breathe=.7+.3*sin(tt*m+ph*2.);",                           // slow ebb and flow
    " float w=(.003+.042*(1.-a)*(1.-a))*(.8+.2*sin(tt*(m+1.)+ph))*(.85+.15*breathe);",
    " vec2 ring=vec2(cos(tt),sin(tt))*1.5;",
    " float v=0.;",
    " for(int j=0;j<3;j++){float fj=float(j);",
    "  float off=(fj-1.)*w*(1.4+4.*(1.-a)*(1.-a))*sin(u*2.4+tt*(1.+fj)+ph+fj*2.);",   // tails split apart
    "  float d=(y-yc-off)/(w*(1.+.35*fj));",
    "  float nz=n(vec2(u*6.+fj*5.,d*.35+ph)+ring)*(.4+.8*n(vec2(u*17.-fj*3.,d*.8)+ring.yx));",
    "  float feather=mix(.25+1.2*nz,.08+1.5*nz,(1.-a)*(1.-a));",          // more broken, feathered at the tail
    "  v+=exp(-d*d)*feather*(1.-.25*fj);}",
    " float halo=exp(-pow((y-yc)/(w*6.),2.))*.1*(1.-a*.6);",
    " return env*(v*.55+halo)*min(sqrt(.007/w),1.4)*(.55+.45*breathe);}",
    "void main(){",
    " vec2 q=gl_FragCoord.xy/r;",
    " vec3 cy=vec3(0.,1.,1.),bl=vec3(.275,.72,1.),pu=vec3(.61,.30,1.),mg=vec3(.91,.235,.96),pearl=vec3(.93,.95,1.);",
    " vec3 col=vec3(0.);",
    //                                      k   y0   ph   slope  W    len  curl  m
    //                                      k   y0   ph   slope  W    len  curl  m      (W*k/240 = speed, ~.025-.03 screens/s)
    " col+=mix(cy,pearl,.45)*ribbon(q.x,q.y,5.,.24,0.,  .18, 1.5,.46,.02, 3.);",
    " col+=mix(pu,pearl,.25)*ribbon(q.x,q.y,5.,.62,2.1,-.28, 1.45,.4, .03, 2.);",
    " col+=mix(bl,pearl,.3) *ribbon(q.x,q.y,4.,.44,4.3, .04, 1.55,.5, .0, 4.)*.9;",
    " #if " + RIB + " > 3",
    " col+=mix(mg,pearl,.3) *ribbon(q.x,q.y,5.,.82,1.2,-.1, 1.4,.38,.025,3.);",
    " col+=mix(cy,pu,.5)*ribbon(q.x,q.y,5.,.12,5.6, .3,  1.35,.34, .03, 5.)*.8;",
    " #endif",
    " col*=.6;",
    " col+=(h(gl_FragCoord.xy+fract(t*7.))-.5)/255.;",
    " gl_FragColor=vec4(max(col,0.),1.);}"
  ].join("\n");

  function sh(type, src) { var o = gl.createShader(type); gl.shaderSource(o, src); gl.compileShader(o); return gl.getShaderParameter(o, gl.COMPILE_STATUS) ? o : null; }
  var v = sh(gl.VERTEX_SHADER, vs), f = sh(gl.FRAGMENT_SHADER, fs);
  if (!v || !f) { root.classList.add("no-gl"); return; }
  var pr = gl.createProgram(); gl.attachShader(pr, v); gl.attachShader(pr, f); gl.linkProgram(pr);
  if (!gl.getProgramParameter(pr, gl.LINK_STATUS)) { root.classList.add("no-gl"); return; }
  gl.useProgram(pr);
  gl.bindBuffer(gl.ARRAY_BUFFER, gl.createBuffer());
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
  var a = gl.getAttribLocation(pr, "a"); gl.enableVertexAttribArray(a); gl.vertexAttribPointer(a, 2, gl.FLOAT, false, 0, 0);
  var uR = gl.getUniformLocation(pr, "r"), uT = gl.getUniformLocation(pr, "t");

  // Soft smoke upscales cleanly, so render well below screen resolution.
  var scale = phone ? 0.35 : 0.55;
  function size() {
    var dpr = Math.min(window.devicePixelRatio || 1, 1.5);
    var w = Math.max(1, Math.round(innerWidth * dpr * scale)), h = Math.max(1, Math.round(innerHeight * dpr * scale));
    if (cv.width !== w || cv.height !== h) { cv.width = w; cv.height = h; gl.viewport(0, 0, w, h); }
    gl.uniform2f(uR, w, h);
  }
  var m = /vseed=(\d+)/.exec(location.hash), t0 = performance.now(), seed = m ? +m[1] : Math.random() * L, last = 0, raf = 0;
  function draw(now) {
    gl.uniform1f(uT, (seed + (still ? 0 : (now - t0) / 1000)) % L);
    gl.drawArrays(gl.TRIANGLES, 0, 3);
  }
  function loop(now) {
    raf = requestAnimationFrame(loop);
    if (now - last < 33) return; // ~30 fps is plenty for slow vapor
    last = now; draw(now);
  }
  function start() { if (!raf && !still && !document.hidden) raf = requestAnimationFrame(loop); }
  function stop() { cancelAnimationFrame(raf); raf = 0; }
  size(); draw(performance.now()); root.classList.add("gl-on");
  addEventListener("resize", function () { size(); if (still) draw(performance.now()); });
  document.addEventListener("visibilitychange", function () { document.hidden ? stop() : start(); });
  cv.addEventListener("webglcontextlost", function (e) { e.preventDefault(); stop(); root.classList.add("no-gl"); });
  start();
})();
