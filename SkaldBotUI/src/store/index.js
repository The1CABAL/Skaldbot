import Vue from "vue";
import Vuex from "vuex";
import forms from './modules/forms';
import authentication from './modules/authentication'
import account from './modules/account'
import documentation from './modules/Documentation'
import suggestions from './modules/suggestions'
import servers from './modules/servers'
import github from './modules/github'
import page from './modules/page'

Vue.use(Vuex);

export default new Vuex.Store({
    modules: {
        authentication,
        forms,
        account,
        documentation,
        suggestions,
        servers,
        github,
        page
    }
});