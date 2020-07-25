import Vue from 'vue';

import { router } from './helpers';
import store from './store';
import App from './App';
import VueFormGenerator from 'vue-form-generator'
import fieldPassword from './components/CustomFields/fieldPassword';
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import lang from 'element-ui/lib/locale/lang/en'
import locale from 'element-ui/lib/locale'
import VueDataTables from 'vue-data-tables'

locale.use(lang)

Vue.component("fieldPassword", fieldPassword);

Vue.use(ElementUI)
Vue.use(VueFormGenerator);
Vue.use(VueDataTables)

new Vue({
    el: '#app',
    router,
    store,
    render: h => h(App)
});