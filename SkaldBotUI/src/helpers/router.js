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
        { path: '/home', name: "home", component: HomePage },
        { path: '/login', name: "login", component: Login },
        { path: '/register', name: "register", component: Register },
        { path: '/about', component: About },
        { path: '/suggestions', component: Suggestions },
        {
            path: '/dashboard', component: Dashboard, redirect: '/dashboardhome',
            children: [
                {
                    path: '/dashboardhome', name: "dashboardhome", component: DashboardHome
                },
                {
                    path: '/manageusers', name: "manageusers", component: ManageUsers
                },
                {
                    path: '/pendingitems', name: "pendingitems", component: PendingItems
                },
                {
                    path: '/managestories', name: "managestories", component: ManageStories
                },
                {
                    path: '/managewisdoms', name: "managewisdoms", component: ManageWisdoms
                },
                {
                    path: '/manageforms', name: "manageforms", component: ManageForms
                },
                {
                    path: '/managedocumentation', name: "managedocumentation", component: ManageDocumentation
                },
                {
                    path: '/github', name: "github", beforeEnter() {
                        window.open("https://github.com/The1CABAL/SkaldBot/projects/1", '_blank')
                    }
                },
                {
                    path: '/modifyform', name: "modifyform", component: ModifyForm
                },
                {
                    path: '/modifyform/:formKey', name: "modifyform", component: ModifyForm, props: true
                }]
        },
        { path: '/userprofile/:userId', name: 'userprofile', component: UserProfile, props: true },
        { path: '/accountprofile/:accountId', name: 'accountprofile', component: AccountProfile, props: true },
        { path: '/registerUser/:accountId', name: 'registeraccountuser', component: RegisterUser, props: true },
        { path: '/manageserver', name: 'manageserver', component: ManageServer },
        { path: '/unauthorized', component: Unauthorized },

        // otherwise redirect to home
        { path: '*', redirect: '/home' },
    ],
    linkExactActiveClass: "activeLink"
});