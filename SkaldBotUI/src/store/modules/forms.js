import axios from 'axios';
import { BaseUrl } from '../../helpers/constants'
const state = {
    forms: [],
    form: []
};

const getters = {
    allForms: state => state.forms,
    getForm: state => state.form
};

const actions = {
    async fetchAllForms({ commit }) {
        const response = await axios.get(
            BaseUrl + 'getForms'
        );

        commit('setForms', JSON.parse(response.data));
    },

    async fetchAllFormsByPageId({ commit }, pageId) {
        const response = await axios.get(
            BaseUrl + `getFormByPageId?pageId=${pageId}`
        );

        commit('setForms', JSON.parse(response.data));
    },

    async fetchFormByFormKey({ commit }, formKey) {
        const response = await axios.get(
            BaseUrl + `form?formKey=${formKey}`
        );

        commit('setForm', JSON.parse(response.data));
    },

    async updateForm({ commit }, formData) {
        return new Promise((resolve, reject) => {
            let url = BaseUrl + 'form'
            axios.post(url, formData).then(resp => {
                resolve(resp)
            }).catch(err => {
                reject(err);
            })
        })
    }
};

const mutations = {
    setForms: (state, forms) => (state.forms = forms),
    setForm: (state, form) => (state.form = form)
};

export default {
    state,
    getters,
    actions,
    mutations
};