import axios from 'axios';
import { BaseUrl } from '../../helpers/constants';

const state = {
    accountInformation: [],
    users: []
}

const getters = {
    accountInformation: state => state.accountInformation,
    accountUsers: state => state.users
}

const actions = {
    async getAccountInformation({ commit }, accountId) {
        return new Promise((resolve, reject) => {
            let url = BaseUrl + `account`
            axios.get(url, {
                params: {
                    accountId
                }
            }).then(resp => {
                commit('set_account_information', resp.data)
                resolve(resp);
            }).catch(err => {
                commit('auth_error')
                reject(err);
            })
        })
    },

    async getAccountUsers({ commit }, model) {
        return new Promise((resolve, reject) => {
            let url = `${BaseUrl}accountUsers`

            axios.get(url, {
                params: {
                    ...model
                }
            }).then(resp => {
                commit('set_account_users', resp.data)
                resolve(resp);
            }).catch(err => {
                commit('auth_error')
                reject(err)
            })
        })    
    },

    async updateAccountInformation({ commit }, account) {
        return new Promise((resolve, reject) => {
            let url = BaseUrl + 'account'
            axios.post(url, account).then(resp => {
                commit('set_account_information', resp.data)
                resolve(resp)
            }).catch(err => {
                commit('auth_error')
                reject(err);
            })
        })
    }
}

const mutations = {
    set_account_information(state, data) {
        state.accountInformation = JSON.parse(data)[0];
    },

    set_account_users(state, data) {
        if (data.length <= 0) {
            return;
        }

        if (data.length == 1) {
            const totalRecords = JSON.parse(data[0]);
            state.users = { ...totalRecords };
        }

        const items = JSON.parse(data[0]);
        const totalRecords = JSON.parse([data[1]]);

        state.users = { ...items, ...totalRecords }
    },

    auth_error(state) {
        state.accountInformation = [];
        state.users = [];
    }
}

export default {
    state,
    getters,
    actions,
    mutations
}