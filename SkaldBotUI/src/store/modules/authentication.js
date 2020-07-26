import Vue from 'vue'
import axios from 'axios';
import { BaseUrl } from '../../helpers/constants';

Vue.prototype.$http = axios
const token = localStorage.getItem('token')
if (token) {
    Vue.prototype.$http.defaults.headers.common['Authorization'] = token
}

const state = {
    token: localStorage.getItem('token') || '',
    status: '',
    user: [],
    isMasterAdmin: localStorage.getItem('isMasterAdmin') || false,
    isAdmin: localStorage.getItem('isAdmin') || false,
    isUser: true
};

const getters = {
    isLoggedIn: state => !!state.token,
    authStatus: state => state.status,
    isMasterAdmin: state => state.isMasterAdmin,
    isAdmin: state => state.isAdmin,
    isUser: state => state.isUser
};

const actions = {
    async login({ commit }, user) {
        //console.log(user);
        let baseUser = user;
        return new Promise((resolve, reject) => {
            commit('auth_request')
            let url = BaseUrl + 'login'
            axios.post(url, user).then(resp => {
                const token = resp.data.token
                const user = resp.data.user
                //console.log(token);
                localStorage.setItem('token', token)
                axios.defaults.headers.common['Authorization'] = token
                commit('auth_success', token, user)

                var userUrl = BaseUrl + 'roles?username=' + baseUser.username
                axios.get(userUrl).then(resp => {
                    const role = JSON.parse(resp.data);
                    commit('user_roles', role[0].Role)
                    resolve(resp)
                })
                    .catch(err => {
                        commit('auth_error')
                        localStorage.removeItem('token')
                        reject(err)
                    });

                resolve(resp)
            })
                .catch(err => {
                    commit('auth_error')
                    localStorage.removeItem('token')
                    reject(err)
                });
        })
    },
    async register({ commit }, user) {
        return new Promise((resolve, reject) => {
            commit('auth_request')
            let url = BaseUrl + 'register'
            axios.post(url, user).then(resp => {
                const token = resp.data.token
                const user = resp.data.user
                localStorage.setItem('token', token)
                axios.defaults.headers.common['Authorization'] = token
                commit('auth_success', token, user)
                resolve(resp)
            })
                .catch(err => {
                    commit('auth_error')
                    localStorage.removeItem('token')
                    reject(err)
                })
        })
    },
    logout({ commit }) {
        return new Promise((resolve, reject) => {
            commit('logout')
            localStorage.removeItem('token')
            delete axios.defaults.headers.common['Authorization']
            resolve()
        })
    }
};

const mutations = {
    auth_request(state) {
        state.status = 'loading'
    },
    auth_success(state, token, user) {
        state.status = 'success'
        state.token = token
        state.user = user
    },
    user_roles(state, role) {
        if (role == "MasterAdmin") {
            localStorage.setItem('isMasterAdmin', true)
        }
        if (role == "Admin") {
            localStorage.setItem('isAdmin', true)
        }
    },
    auth_error(state) {
        state.status = 'error'
    },
    logout(state) {
        state.status = ''
        state.token = ''
        state.isMasterAdmin = false
        localStorage.removeItem('isMasterAdmin')
        state.isAdmin = false
        localStorage.removeItem('isAdmin')
        state.isUser = true
    },
};

export default {
    state,
    getters,
    actions,
    mutations
};