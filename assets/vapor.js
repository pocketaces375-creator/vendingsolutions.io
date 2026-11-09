/* Vending Solutions: slow drifting vapor background (WebGL fbm, CSS fallback). */
(function () {
  var cv = document.getElementById("vapor");
  if (!cv) return;
  var root = document.documentElement;
  var still = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var phone = Math.min(screen.width, screen.height) < 700 || /Mobi|Android/i.test(navigator.userAgent);
  var gl = cv.getContext("webgl", { alpha: false, antialias: false, depth: false, powerPreference: "low-power" });
  if (!gl) { root.classList.add("no-gl"); return; }

  var N = phone ? 6 : 12;
  var vs = "attribute vec2 a;void main(){gl_Position=vec4(a,0.,1.);}";
  // Seamless loop: noise is periodic in x and every motion repeats exactly every L seconds,
  // and JS feeds t modulo L, so the drift never resets or cuts.
  var L = 240.0;
  // Small vapor wisps that rise, sway and dissolve, scattered across the screen.
  // Each wisp lives k times per 240 s loop (k integer) and respawns at a new random spot only while
  // fully faded out, and the respawn pattern repeats every loop, so there is never a visible cut.
  // The layer is fixed to the viewport and ignores page scroll on purpose (comfort).
  var fs = [
    "#ifdef GL_FRAGMENT_PRECISION_HIGH\nprecision highp float;\n#else\nprecision mediump float;\n#endif",
    "uniform vec2 r;uniform float t;",
    "const float L=" + L.toFixed(1) + ";const float TAU=6.2831853;",
    "float h(vec2 p){p=fract(p*vec2(.1031,.1030));p+=dot(p,p.yx+33.33);return fract((p.x+p.y)*p.x);}",
    "float n(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);",
    " return mix(mix(h(i),h(i+vec2(1,0)),f.x),mix(h(i+vec2(0,1)),h(i+1.),f.x),f.y);}",
    "vec3 pal(float x){vec3 cy=vec3(0.,1.,1.),bl=vec3(.275,.72,1.),pu=vec3(.61,.30,1.),mg=vec3(.91,.235,.96);",
    " return x<.3?cy:x<.55?bl:x<.8?pu:mg;}",
    "void main(){",
    " float ar=r.x/r.y; vec2 p=vec2(gl_FragCoord.x/r.y,gl_FragCoord.y/r.y);",   // y: 0 bottom .. 1 top
    " float tt=TAU*t/L; vec2 ring=vec2(cos(tt),sin(tt))*1.5;",
    " vec3 pearl=vec3(.93,.95,1.); vec3 col=vec3(0.);",
    " for(int i=0;i<" + N + ";i++){",
    "  float fi=float(i);",
    "  float k=6.+floor(h(vec2(fi,3.1))*5.);",                     // 6..10 lives per loop: 24-40 s each
    "  float ph=h(vec2(fi,7.7));",
    "  float cyc=k*t/L+ph; float c=mod(floor(cyc),k); float age=fract(cyc);",
    "  float r1=h(vec2(fi*1.3+c,1.)),r2=h(vec2(c*2.1,fi+5.)),r3=h(vec2(fi+c*.7,9.)),r4=h(vec2(c+fi*3.3,2.));",
    "  float life=smoothstep(0.,.25,age)*smoothstep(1.,.5,age);",  // fade in, then dissolve while climbing
    "  float len=.18+.22*r4;",
    "  float y0=-.05+.75*r2;",
    "  float head=y0+(.32+.3*r3)*age+len*.5;",                      // slow rise: ~.01-.025 screen heights/s
    "  float v=(head-p.y)/len;",                                     // 0 = top (dissolving), 1 = bottom (source)
    "  if(v<0.||v>1.)continue;",
    "  float lean=(r3-.5)*1.1;",                                     // 50-90 deg from horizontal, either side
    "  float sway=(.012+.03*(1.-v))*sin(p.y*9.+tt*(3.+fi)+fi*2.)+.008*sin(p.y*23.-tt*5.+fi);",
    "  float xc=.04*ar+r1*ar*.92+lean*(p.y-y0)+sway;",
    "  float w=(.0025+.018*(1.-v)*(1.-v))*(.7+.6*age);",           // thin near the source, spreading as it rises
    "  if(abs(p.x-xc)>w*9.)continue;",
    "  float env=smoothstep(0.,.35,v)*smoothstep(1.,.7,v);",
    "  float s=0.;",
    "  for(int j=0;j<3;j++){float fj=float(j);",
    "   float off=(fj-1.)*w*(1.2+3.5*(1.-v))*sin(p.y*6.+tt*(2.+fj)+fi+fj*2.);",
    "   float d=(p.x-xc-off)/(w*(1.+.35*fj));",
    "   float nz=n(vec2(d*.35+fi,p.y*9.+fj*5.)-ring)*(.4+.8*n(vec2(d*.8,p.y*26.-fj*3.)+ring.yx));",
    "   s+=exp(-d*d)*(.15+1.3*nz)*(1.-.25*fj);}",
    "  float halo=exp(-pow((p.x-xc)/(w*6.),2.))*.08;",
    "  vec3 tint=mix(pal(h(vec2(fi,c+.5))),pearl,.3+.25*r4);",
    "  col+=tint*env*life*(s*.5+halo)*min(sqrt(.006/w),1.4);",
    " }",
    " col*=.38;",
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
