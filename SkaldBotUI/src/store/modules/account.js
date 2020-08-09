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
    async getAccountInformation({ commit }, accountInfo) {
        return new Promise((resolve, reject) => {
            let url = BaseUrl + `account?accountId=${accountInfo.accountId}&isMaster=${accountInfo.isMasterAdmin}`
            axios.get(url).then(resp => {
                commit('set_account_information', resp.data)
                resolve(resp);
            }).catch(err => {
                commit('auth_error')
                reject(err);
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
        state.accountInformation = JSON.parse(data[0])[0];
        state.users = JSON.parse(data[1]);
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