import Vue from 'vue';
import Router from 'vue-router';

import HomePage from '../home/HomePage'
import About from '../home/About'

Vue.use(Router);

export const router = new Router({
    mode: 'history',
    routes: [
        { path: '/', component: HomePage },
        { path: '/about', component: About },

        // otherwise redirect to home
        { path: '*', redirect: '/' }
    ],
    linkExactActiveClass: "activeLink"
});