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
    accountId: localStorage.getItem('accountId') || '',
    status: '',
    isMasterAdmin: false,
    isAdmin: false,
    isClientAdmin: false,
    isClientUser: false,
    isUser: true,
    role: '',
    user: {}
};

const getters = {
    userId: state => state.token,
    accountId: state => state.accountId,
    isLoggedIn: state => state.token != '' ? true : false,
    authStatus: state => state.status,
    isMasterAdmin: state => state.role == "MasterAdmin" ? true : false,
    isAdmin: state => state.role == "Admin" ? true : false,
    isClientAdmin: state => state.Role == "ClientAdmin" ? true : false,
    isClientUser: state => state.role = "ClientUser" ? true : false,
    isUser: state => state.isUser,
    user: state => state.user
};

const actions = {
    async login({ commit }, user) {
        return new Promise((resolve, reject) => {
            commit('auth_request')
            let url = BaseUrl + 'login'
            axios.post(url, user).then(resp => {
                const token = JSON.parse(resp.data)[0].Id
                const accountId = JSON.parse(resp.data)[0].AccountId
                const username = JSON.parse(resp.data)[0].Username
                const user = { accountId, username }
                localStorage.setItem('token', token)
                localStorage.setItem('accountId', accountId)
                console.log(localStorage.getItem('accountId'))
                axios.defaults.headers.common['Authorization'] = token
                commit('auth_success', token, user)

                var userUrl = BaseUrl + 'roles?id=' + token
                axios.get(userUrl).then(resp => {
                    const role = JSON.parse(resp.data);
                    commit('user_roles', role[0].Role)
                    resolve(resp)
                })
                    .catch(err => {
                        commit('auth_error')
                        localStorage.removeItem('token')
                        localStorage.removeItem('accountId');
                        reject(err)
                    });

                resolve(resp)
            })
                .catch(err => {
                    commit('auth_error')
                    localStorage.removeItem('token')
                    localStorage.removeItem('accountId');
                    reject(err)
                });
        })
    },
    async register({ commit }, user) {
        return new Promise((resolve, reject) => {
            commit('auth_request')
            let url = BaseUrl + 'register'
            axios.post(url, user).then(resp => {
                resolve(resp)
            })
                .catch(err => {
                    commit('auth_error')
                    reject(err)
                })
        })
    },
    async registeruser({ commit }, user) {
        return new Promise((resolve, reject) => {
            commit('auth_request')
            let url = BaseUrl + 'registeruser'
            axios.post(url, user).then(resp => {
                resolve(resp)
            })
                .catch(err => {
                    commit('auth_error')
                    reject(err)
                })
        })
    },
    async loadRoles({ commit }) {
        var userId = this.getters.userId;
        var userUrl = BaseUrl + 'roles?id=' + userId

        return new Promise((resolve, reject) => {
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
        })
    },
    logout({ commit }) {
        return new Promise((resolve, reject) => {
            commit('logout')
            localStorage.removeItem('token')
            localStorage.removeItem('accountId');
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
        state.role = role
    },
    auth_error(state) {
        state.status = 'error'
    },
    logout(state) {
        state.status = ''
        state.token = ''

        localStorage.removeItem('token');
        localStorage.removeItem('accountId');

        state.isMasterAdmin = false
        state.isAdmin = false
        state.isClientAdmin = false
        state.isClientUser = false
        state.isUser = true
    },
};

export default {
    state,
    getters,
    actions,
    mutations
};