!function(e,t){if("object"==typeof exports&&"object"==typeof module)module.exports=t();else if("function"==typeof define&&define.amd)define([],t);else{var r=t();for(var o in r)("object"==typeof exports?exports:e)[o]=r[o]}}(self,(()=>(()=>{"use strict";var e={d:(t,r)=>{for(var o in r)e.o(r,o)&&!e.o(t,o)&&Object.defineProperty(t,o,{enumerable:!0,get:r[o]})},o:(e,t)=>Object.prototype.hasOwnProperty.call(e,t),r:e=>{"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})}},t={};function r(e){return new Promise((t=>setTimeout(t,e)))}function o(e){let t=document.createElement("div");return t.innerHTML=e,t.firstElementChild}function n(e,t){return r=e.dataset,t.jsName in r;var r}function s(e,t){return e.dataset[t.jsName]}e.r(t),e.d(t,{createElementFromHTML:()=>o,runWithContext:()=>g,sleep:()=>r});class l{jsName;htmlAttribute;constructor(e){this.htmlAttribute="data-e-"+e,this.jsName="e"+e.replace(/(?:^|-)(\w)/g,((e,t)=>t.toUpperCase()))}}const i=new l("onclick"),a=new l("onsubmit"),c=new l("oninput"),u=new l("onchange"),f=new l("name"),p=new l("scope"),m=new l("progress"),d=new l("progress-target");class h{constructor(e){this.elements={};let t=[],r=e.closest(`[${p.htmlAttribute}]`);for(;r;)t.push(r),r=r.parentElement?.closest(`[${p.htmlAttribute}]`);t.push(document);for(let e of t.reverse()){let t=Array.from(e.querySelectorAll(`[${f.htmlAttribute}]`));e instanceof HTMLElement&&e.matches(`[${f.htmlAttribute}]`)&&t.push(e);for(let e of t.reverse())this.elements[s(e,f)]=e}}}class b{static _states=[];static pushContext(e){let t={};for(let[r,o]of Object.entries(e.elements)){Object.prototype.hasOwnProperty(globalThis,r)?t[r]=globalThis[r]:t[r]=void 0;try{globalThis[r]=o}catch{}}this._states.push(t)}static popContext(){let e=this._states.pop();if(e)for(let[t,r]of Object.entries(e))try{void 0===r?delete globalThis[t]:globalThis[t]=r}catch{}}}const y=(async()=>{}).constructor;async function g(e,t={}){let{target:r,args:o}=t;r=r||document.body;let l=new h(r),i=function(e,t){let r=[];if(n(e,m)){let o=e;if(n(e,d)){let r=s(e,d);o=t[r]||o}let l=new Set(s(e,m).split(",").map((e=>e.trim())));for(let e of l)"disable"===e&&(o.disabled=!0,r.push((()=>o.disabled=!1)))}return()=>r.forEach((e=>e()))}(r,l);try{return b.pushContext(l),o=o||[],e instanceof y?await e(...o):e(...o)}finally{b.popContext(),i()}}function w(e,t){document.addEventListener(e,(async e=>{let r=e.target;if(r=r.closest(`[${t.htmlAttribute}]`),!r)return;let o=s(r,t),n=window[s(r,t)];if(!n)throw new Error(`Handler '${o}' not found`);return await g(n,{target:r,args:[e]})}))}return w("submit",a),w("click",i),w("input",c),w("change",u),t})()));
//# sourceMappingURL=bindings.js.map