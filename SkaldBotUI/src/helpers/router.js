import Vue from 'vue';
import Router from 'vue-router';

import Login from '../account/Login'
import Register from '../account/Register'
import HomePage from '../home/HomePage'
import About from '../home/About'
import Suggestions from '../home/Suggestions'
import Dashboard from '../secured/Dashboard/Dashboard'
import ManageUsers from '../secured/Dashboard/ManageUsers'
import Unauthorized from '../secured/Unauthorized'
import DashboardHome from '../secured/Dashboard/DashboardHome'
import UserProfile from '../secured/user/UserProfile'

Vue.use(Router);

export const router = new Router({
    mode: 'history',
    routes: [
        { path: '/home', name: "home", component: HomePage },
        { path: '/login', name: "login", component: Login },
        { path: '/register', name: "register", component: Register },
        { path: '/about', component: About },
        { path: '/suggestions', component: Suggestions },
        { path: '/dashboard', component: Dashboard, redirect: '/dashboardhome', children: [{ path: '/dashboardhome', name: "dashboardhome", component: DashboardHome }, { path: '/manageusers', name: "manageusers", component: ManageUsers }] },
        { path: '/userprofile/:userId', name:'userprofile', component: UserProfile, props: true },
        { path: '/unauthorized', component: Unauthorized },

        // otherwise redirect to home
        { path: '*', redirect: '/home' },
    ],
    linkExactActiveClass: "activeLink"
});