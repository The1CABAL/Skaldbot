import Vue from 'vue';

import { router } from './helpers';
import store from './store';
import App from './App';


import VueFormGenerator from 'vue-form-generator'
Vue.use(VueFormGenerator);

import './validators.js'

import fieldPassword from './components/vfgFields/vfgPassword';
Vue.component("field-password", fieldPassword);

import vfgInput from './components/vfgFields/vfgInput';
Vue.component("field-vue-input", vfgInput);

import vfgButton from './components/vfgFields/vfgButton';
Vue.component("field-vue-button", vfgButton);

import vfgCheckbox from './components/vfgFields/vfgCheckbox';
Vue.component("field-vue-checkbox", vfgCheckbox);

import vfgTextArea from './components/vfgFields/vfgTextArea';
Vue.component("field-vue-textarea", vfgTextArea);

import vfgSelect from './components/vfgFields/vfgSelect';
Vue.component("field-vue-select", vfgSelect);

import './style/styles.css'

import * as Tabs from 'vue-slim-tabs'
//import 'vue-slim-tabs/themes/default.css'
Vue.use(Tabs)

new Vue({
    el: '#app',
    router,
    store,
    render: h => h(App)
});