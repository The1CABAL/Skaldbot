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
    user: {},
    userData: [],
    roles: [],
    users: []
};

const getters = {
    userId: state => state.token,
    getAccountId: state => state.accountId,
    isLoggedIn: state => state.token != '' ? true : false,
    authStatus: state => state.status,
    isMasterAdmin: state => state.role == "MasterAdmin" ? true : false,
    isAdmin: state => state.role == "Admin" ? true : false,
    isClientAdmin: state => state.role == "ClientAdmin" ? true : false,
    isClientUser: state => state.role = "ClientUser" ? true : false,
    isUser: state => state.isUser,
    user: state => state.user,
    getUser: state => state.userData,
    getUsers: state => state.users,
    getAllRoles: state => state.roles,
    getRole: state => state.role
};

const actions = {
    async login({ commit }, user) {
        return new Promise((resolve, reject) => {
            commit('auth_request');

            let url = BaseUrl + 'login'
            axios.post(url, user).then(resp => {
                const token = JSON.parse(resp.data)[0].Id
                const accountId = JSON.parse(resp.data)[0].AccountId
                const username = JSON.parse(resp.data)[0].Username
                const user = { token, accountId, username }
                localStorage.setItem('token', token)
                localStorage.setItem('accountId', accountId)
                axios.defaults.headers.common['Authorization'] = token
                commit('auth_success', user)

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
                    console.log(err);
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
    async getAllUsers({ commit }, model) {
        let url = `${BaseUrl}getUsers`;
        return new Promise((resolve, reject) => {
            axios.get(url, {
                params: {
                    ...model
                }
            }).then(resp => {
                commit('set_users', resp.data);
                resolve(resp);
            }).catch(err => {
                console.log(err);
                reject(err);
            })
        })
    },
    async getUser({ commit }, userId) {
        let url = BaseUrl + 'getUser?userId=' + userId
        return new Promise((resolve, reject) => {
            axios.get(url).then(resp => {
                commit('set_user_data', resp.data);
                resolve(resp);
            }).catch(err => {
                console.log(err);
                reject(err);
            })
        })
    },
    async getAllRoles({ commit }) {
        let url = BaseUrl + 'getRoles'
        return new Promise((resolve, reject) => {
            axios.get(url).then(resp => {
                commit('set_all_roles', resp.data);
                resolve(resp);
            }).catch(err => {
                console.log(err);
                reject(err);
            })
        })
    },
    async updateUser({ commit }, userData) {
        let url = BaseUrl + 'getUser';
        return new Promise((resolve, reject) => {
            axios.post(url, userData).then(resp => {
                commit('set_status', resp.data);
                resolve(resp);
            }).catch(err => {
                console.log(err);
                reject(err);
            })
        })
    },
    logout({ commit }) {
        return new Promise((resolve, reject) => {
            commit('logout')
            delete axios.defaults.headers.common['Authorization']
            resolve()
        })
    }
};

const mutations = {
    auth_request(state) {
        state.status = 'loading'
    },
    auth_success(state, user) {
        state.status = 'success'
        state.token = user.token
        var accountId = user.accountId;
        var username = user.username;
        state.user = { accountId, username }
        state.accountId = accountId
    },
    user_roles(state, role) {
        state.role = role
    },
    auth_error(state) {
        state.status = 'error'
    },
    set_users(state, users) {
        if (users.length <= 0) {
            return;
        }

        if (users.length === 1) {
            const totalRecords = JSON.parse(users[0]);
            state.users = { ...totalRecords };
            return;
        }

        const userData = JSON.parse(users[0]);
        const totalRecords = JSON.parse(users[1])

        state.users = { ...userData, ...totalRecords }

    },
    set_user_data(state, user) {
        state.userData = JSON.parse(user)[0]
    },
    set_all_roles(state, roles) {
        state.roles = JSON.parse(roles);
    },
    set_status(state, status) {
        state.status = status.Message.toString();
    },
    logout(state) {
        state.status = ''
        state.token = ''
        state.role = ''

        localStorage.removeItem('token');
        localStorage.removeItem('accountId');

        state.accountId = '';

        state.isMasterAdmin = false;
        state.isAdmin = false;
        state.isClientAdmin = false;
        state.isClientUser = false;
        state.isUser = true;
        state.isLoggedIn = false;
    },
};

export default {
    state,
    getters,
    actions,
    mutations
};