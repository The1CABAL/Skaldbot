import axios from 'axios';
import { BaseUrl } from '../../helpers/constants';
import JSONbig from 'json-bigint'

const state = {
    server: [],
    servers: []
};

const getters = {
    getServers: state => state.servers,
    getServer: state => state.server
};

const actions = {
    async getAccountServers({ commit }, accountId) {
        let url = BaseUrl + 'accountServers?accountId=' + accountId
        return new Promise((resolve, reject) => {
            axios.get(url).then(resp => {
                commit('set_servers', resp.data);
                resolve(resp);
            }).catch(err => {
                console.log(err);
                reject(err);
            })
        })
    },
    async getServerById({ commit }, serverId) {
        let url = BaseUrl + 'server?id=' + serverId
        return new Promise((resolve, reject) => {
            axios.get(url).then(resp => {
                commit('set_server', resp.data);
                resolve(resp);
            }).catch(err => {
                console.log(err);
                reject(err);
            })
        })
    }
};

const mutations = {
    set_servers(state, servers) {
        if (servers.length > 0) {
            state.servers = JSONbig.parse(servers);
        }
    },
    set_server(state, server) {
        state.server = JSONbig.parse(server)[0];
    }
};

export default {
    state,
    getters,
    actions,
    mutations
}