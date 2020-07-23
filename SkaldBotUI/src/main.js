import Vue from 'vue';

import { router } from './helpers';
import store from './store';
import App from './App';
import VueFormGenerator from 'vue-form-generator'
import fieldPassword from './components/CustomFields/fieldPassword';

Vue.component("fieldPassword", fieldPassword);

Vue.use(VueFormGenerator);

new Vue({
    el: '#app',
    router,
    store,
    render: h => h(App)
});