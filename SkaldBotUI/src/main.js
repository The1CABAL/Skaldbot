import Vue from 'vue';

import { router } from './helpers';
import store from './store';
import App from './App';

new Vue({
    el: '#app',
    router,
    store,
    render: h => h(App)
});