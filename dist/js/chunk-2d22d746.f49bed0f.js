(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-2d22d746"],{f820:function(t,n,a){"use strict";a.r(n);var o=function(){var t=this,n=t.$createElement,a=t._self._c||n;return a("div",{staticClass:"about"},[a("v-container",[t.about?a("div",{domProps:{innerHTML:t._s(t.about)}}):t._e()])],1)},u=[],e={data:function(){return{about:""}},methods:{loadAbout:function(){var t=this;this.$http.get(this.$HOST+"/api/get/static/about",{withCredentials:!0}).then((function(n){t.about=n.data.val}))}},mounted:function(){this.loadAbout()}},i=e,s=a("2877"),c=Object(s["a"])(i,o,u,!1,null,null,null);n["default"]=c.exports}}]);
//# sourceMappingURL=chunk-2d22d746.f49bed0f.js.map