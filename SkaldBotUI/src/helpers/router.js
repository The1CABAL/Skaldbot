import Vue from 'vue';
import Router from 'vue-router';

import Login from '../home/Login'
import HomePage from '../home/HomePage'
import About from '../home/About'
import Suggestions from '../home/Suggestions'

Vue.use(Router);

export const router = new Router({
    mode: 'history',
    routes: [
        { path: '/home', name: "home", component: HomePage },
        { path: '/login', name: "login", component: Login },
        { path: '/about', component: About },
        { path: '/suggestions', component: Suggestions },

        // otherwise redirect to home
        { path: '*', redirect: '/home' }
    ],
    linkExactActiveClass: "activeLink"
});