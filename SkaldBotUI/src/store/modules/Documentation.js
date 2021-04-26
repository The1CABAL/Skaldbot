import axios from 'axios';
import { BaseUrl } from '../../helpers/constants';

const state = {
    helpTitle: '',
    helpContent: '',
    isActive: true,
    helpDocumentation: []
};

const getters = {
    helpTitle: state => state.helpTitle,
    helpContent: state => state.helpContent,
    helpIsActive: state => state.isActive,
    helpDocumentation: state => state.helpDocumentation
};

const actions = {
    async getDocumentation({ commit }, docInfo) {
        return new Promise((resolve, reject) => {
            let url = BaseUrl + 'documentation?helpContentKey=' + docInfo.HelpContentKey + "&isAdmin=" + docInfo.IsAdmin
            axios.get(url).then(resp => {
                commit('set_documentation', resp.data)
                resolve(resp);
            }).catch(err => {
                reject(err);
            })
        })
    },
    async getAllDocumentation({ commit }, model) {
        return new Promise((resolve, reject) => {
            let url = BaseUrl + 'getAllDocumentation'
            axios.get(url, {
                params: {
                    ...model
                }
            }).then(resp => {
                commit('set_all_documentation', resp.data)
                resolve(resp);
            }).catch(err => {
                reject(err);
            })
        })
    },
    async updateDocumentation({ commit }, content) {
        return new Promise((resolve, reject) => {
            let url = BaseUrl + 'documentation';
            axios.post(url, content).then(resp => {
                commit('set_documentation', resp.data);
                resolve(resp);
            }).catch(err => {
                reject(err);
            })
        })
    }
};

const mutations = {
    set_documentation(state, rawData) {
        var data = JSON.parse(rawData)[0]
        state.helpTitle = data.HelpTitle;
        state.helpContent = data.HelpContent;
        state.isActive = data.IsActive
    },
    set_all_documentation(state, data) {
        if (data.length <= 0) {
            return;
        }

        if (data.length === 1) {
            const totalRecords = JSON.parse(data[0]);
            state.helpDocumentation = { ...totalRecords };
            return;
        }

        const documentationData = JSON.parse(data[0]);
        const totalRecords = JSON.parse(data[1]);
        state.helpDocumentation = { ...documentationData, ...totalRecords }
    }
};

export default {
    state,
    getters,
    actions,
    mutations
}