import axios from 'axios';

const state = {
    forms: []
};

const getters = {
    allForms: state => state.forms,
    formSchema: state => state.formSchema
};

const actions = {
    async fetchAllForms({ commit }) {
        const response = await axios.get(
            'http://127.0.0.1:5000/api/getForms'
        );

        commit('setForms', JSON.parse(response.data));
    }
};

const mutations = {
    setForms: (state, forms) => (state.forms = forms)
};

export default {
    state,
    getters,
    actions,
    mutations
};