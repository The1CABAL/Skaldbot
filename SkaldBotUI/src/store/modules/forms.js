import axios from 'axios';
import { BaseUrl } from '../../helpers/constants'

const state = {
    forms: [],
    form: [],
    postStatus: ''
};

const getters = {
    getFormSchema: state => state.form.FieldInfo.FieldSchema,
    getFormName: state => state.form.FormInfo.FormName,
    getFormActionLink: state => state.form.FieldInfo.ActionLink,
    getShowFormName: state => state.form.FormInfo.ShowFormName,
    getForms: state => state.forms,
    getForm: state => state.form,
    getPostStatus: state => state.postStatus
};

const actions = {
    async fetchAllForms({ commit }) {
        return new Promise((resolve, reject) => {
            let url = BaseUrl + 'getForms';
            axios.get(url).then(resp => {
                commit('set_forms', resp.data);
                resolve(resp);
            }).catch(err => {
                console.log(err);
                reject(err);
            })
        })
    },

    async fetchAllFormsByPageId({ commit }, pageId) {
        return new Promise((resolve, reject) => {
            let url = BaseUrl + 'getFormByPageId?pageId=' + pageId
            axios.get(url).then(resp => {
                commit('set_forms', resp.data);
                resolve(resp);
            }).catch(err => {
                console.log(err);
                reject(err);
            })
        })
    },

    async fetchForm({ commit }, formKey) {
        return new Promise((resolve, reject) => {
            let url = BaseUrl + 'form?formKey=' + formKey
            axios.get(url).then(resp => {
                commit('set_form', resp.data);
                resolve(resp);
            }).catch(err => {
                console.log(err);
                reject(err);
            })
        })
    },

    async updateForm({ commit }, formData) {
        console.log(formData);
        return new Promise((resolve, reject) => {
            let url = BaseUrl + 'form'
            axios.post(url, formData).then(resp => {
                resolve(resp)
            }).catch(err => {
                reject(err);
            })
        })
    },
    async postFormData({ commit }, formData) {
        let url = BaseUrl + formData.url
        let model = formData.model

        return new Promise((resolve, reject) => {
            axios.post(url, model).then(resp => {
                commit('set_post_status', resp.data.Message.toString())
                resolve(resp);
            }).catch(err => {
                console.log(err);
                reject(err);
            })
        })
    }
};

const mutations = {
    set_forms(state, forms) {
        state.forms = JSON.parse(forms);
    },
    set_form(state, form) {
        let fieldInfo = JSON.parse(form);

        if (!fieldInfo) {
            return;
        }

        fieldInfo = fieldInfo[0]

        if (!fieldInfo.Form) {
            return;
        }

        let formData = fieldInfo.Form[0];

        let obj = {
            FieldInfo: fieldInfo,
            FormInfo: formData
        }

        state.form = obj;
    },
    set_post_status(state, message) {
        state.postStatus = message;
    }
};

export default {
    state,
    getters,
    actions,
    mutations
};