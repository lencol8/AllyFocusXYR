import './assets/styles/app.scss'
import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import vuetify from '@/plugins/vuetify'
import Axios from "axios";
import VueTidio from 'vue-tidio';
import firebase from "firebase/app";
import 'firebase/auth';
import 'firebase/firestore';
import axios from "axios";

Vue.config.productionTip = false
Vue.use(VueTidio, { appKey: 'mrfitz40ms117iasqd3tc32q6qair7le' });
Vue.prototype.$http = axios;

var firebaseConfig = {
  apiKey: "AIzaSyDy79q-u4ovKKU_tSEsa6kRajzAJpJGo4U",
  authDomain: "allyfocus-3ef39.firebaseapp.com",
  databaseURL: "https://allyfocus-3ef39.firebaseio.com",
  projectId: "allyfocus-3ef39",
  storageBucket: "allyfocus-3ef39.appspot.com",
  messagingSenderId: "477957217638",
  appId: "1:477957217638:web:5cc6f0df6e69270ceabca7",
  measurementId: "G-39HB8WYK3P"
};

firebase.initializeApp(firebaseConfig);

const VueCookie = require('vue-cookie');
Vue.use(VueCookie);
Vue.use(require('vue-moment'));
Vue.prototype.$http = Axios;
Vue.prototype.$HOST = 'https://api.allyfocus.com';

Vue.prototype.$firebase = firebase;
Vue.prototype.$vue = Vue;

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
