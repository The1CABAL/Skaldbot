import Vue from 'vue';

import { router } from './helpers';
import store from './store';
import App from './App';

import VueFormGenerator from 'vue-form-generator'
Vue.use(VueFormGenerator);

import fieldPassword from './components/CustomFields/fieldPassword';
Vue.component("fieldPassword", fieldPassword);

import ElementUI from 'element-ui'
import 'element-theme-dark';
Vue.use(ElementUI);

import lang from 'element-ui/lib/locale/lang/en'
import locale from 'element-ui/lib/locale'
locale.use(lang);

import VueDataTables from 'vue-data-tables'
Vue.use(VueDataTables);

import * as Tabs from 'vue-slim-tabs'
//import 'vue-slim-tabs/themes/default.css'
Vue.use(Tabs)

new Vue({
    el: '#app',
    router,
    store,
    render: h => h(App)
});