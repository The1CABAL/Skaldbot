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
import PendingItems from '../secured/Dashboard/PendingItems'
import ManageStories from '../secured/Dashboard/ManageStories'
import ManageWisdoms from '../secured/Dashboard/ManageWisdoms'
import ManageForms from '../secured/Dashboard/ManageForms'
import GitHub from '../secured/Dashboard/GitHub'
import ModifyForm from '../secured/Dashboard/ModifyForm'
import AccountProfile from '../secured/user/AccountProfile'
import RegisterUser from '../secured/user/RegisterUser'
import ManageDocumentation from '../secured/Dashboard/ManageDocumentation'
import ManageServer from '../secured/user/ManageServer'

Vue.use(Router);

export const router = new Router({
    mode: 'history',
    routes: [
        { path: '/home', name: "home", component: HomePage, meta: { accessibleLoggedOut: true, accessibleLoggedIn: true } },
        { path: '/login', name: "login", component: Login, meta: { accessibleLoggedOut: true, accessibleLoggedIn: false } },
        { path: '/register', name: "register", component: Register, meta: { accessibleLoggedOut: true, accessibleLoggedIn: false } },
        { path: '/about', name: "about", component: About, meta: { accessibleLoggedOut: true, accessibleLoggedIn: true } },
        { path: '/suggestions', name: "suggestions", component: Suggestions, meta: { accessibleLoggedOut: true, accessibleLoggedIn: true } },
        {
            path: '/dashboard', name:"dashboard", component: Dashboard, redirect: '/dashboardhome', meta: { accessibleLoggedOut: false, accessibleLoggedIn: true },
            children: [
                {
                    path: '/dashboardhome', name: "dashboard home", component: DashboardHome, meta: { accessibleLoggedOut: false, accessibleLoggedIn: true }
                },
                {
                    path: '/manageusers', name: "manage users", component: ManageUsers, meta: { accessibleLoggedOut: false, accessibleLoggedIn: true }
                },
                {
                    path: '/pendingitems', name: "pending items", component: PendingItems, meta: { accessibleLoggedOut: false, accessibleLoggedIn: true }
                },
                {
                    path: '/managestories', name: "manage stories", component: ManageStories, meta: { accessibleLoggedOut: false, accessibleLoggedIn: true }
                },
                {
                    path: '/managewisdoms', name: "manage wisdoms", component: ManageWisdoms, meta: { accessibleLoggedOut: false, accessibleLoggedIn: true }
                },
                {
                    path: '/manageforms', name: "manage forms", component: ManageForms, meta: { accessibleLoggedOut: false, accessibleLoggedIn: true }
                },
                {
                    path: '/managedocumentation', name: "manage documentation", component: ManageDocumentation, meta: { accessibleLoggedOut: false, accessibleLoggedIn: true }
                },
                //{
                //    path: '/github', name: "github", beforeEnter() {
                //        window.open("https://github.com/The1CABAL/SkaldBot/projects/1", '_blank')
                //    }
                //},
                {
                    path: '/github', name: "github", component: GitHub, meta: { accessibleLoggedOut: false, accessibleLoggedIn: true }
                },
                {
                    path: '/modifyform', name: "modify form", component: ModifyForm, meta: { accessibleLoggedOut: false, accessibleLoggedIn: true }
                },
                {
                    path: '/modifyform/:formKey', name: "modify form", component: ModifyForm, props: true, meta: { accessibleLoggedOut: false, accessibleLoggedIn: true }
                }],
        },
        { path: '/userprofile/:userId', name: 'user profile', component: UserProfile, props: true, meta: { accessibleLoggedOut: false, accessibleLoggedIn: true } },
        { path: '/accountprofile/:accountId', name: 'account profile', component: AccountProfile, props: true, meta: { accessibleLoggedOut: false, accessibleLoggedIn: true } },
        { path: '/registerUser/:accountId', name: 'register account user', component: RegisterUser, props: true, meta: { accessibleLoggedOut: false, accessibleLoggedIn: true } },
        { path: '/manageserver', name: 'manage server', component: ManageServer, meta: { accessibleLoggedOut: false, accessibleLoggedIn: true } },
        { path: '/unauthorized', name: 'unauthorized', component: Unauthorized, meta: { accessibleLoggedOut: true, accessibleLoggedIn: true } },

        // otherwise redirect to home
        { path: '*', redirect: '/home' },
    ]
});


router.beforeEach((to, from, next) => {
    if (!to.meta.accessibleLoggedIn && !to.meta.accessibleLoggedOut) {
        console.error(`Route guard for route ${to.name} is not configured correctly!`)
        next({ name: 'home' });
        return;
    }

    if (to.meta.accessibleLoggedIn && to.meta.accessibleLoggedOut) {
        next();
        return;
    }

    const loggedIn = !!window.localStorage.getItem('token');

    if (to.meta.accessibleLoggedIn) {
        if (!loggedIn) {
            next({ name: 'unauthorized' })
            return;
        }

        next();
        return;
    }

    if (to.meta.accessibleLoggedOut) {
        if (!to.meta.accessibleLoggedIn && loggedIn) {
            next({ name: 'home' })
            return;
        }

        next();
        return;
    }
})