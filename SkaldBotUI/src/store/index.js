import Vue from "vue";
import Vuex from "vuex";
import forms from './modules/forms';
import authentication from './modules/authentication'
import account from './modules/account'
import documentation from './modules/Documentation'

Vue.use(Vuex);

export default new Vuex.Store({
    modules: {
        authentication,
        forms,
        account,
        documentation
    }
});