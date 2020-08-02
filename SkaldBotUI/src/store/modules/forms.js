import axios from 'axios';
import { BaseUrl } from '../../helpers/constants'

const state = {
    formSchema: [],
    formActionLink: '',
    formName: '',
    forms: [],
    form: [],
    postStatus: ''
};

const getters = {
    getFormSchema: state => state.formSchema,
    getFormName: state => state.formName,
    getFormActionLink: state => state.formActionLink,
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

    async fetchFormByFormKey({ commit }, formKey) {
        return new Promise((resolve, reject) => {
            let schemaUrl = BaseUrl + 'getFormSchema?formKey=' + formKey;
            let actionUrl = BaseUrl + 'getActionLink?formKey=' + formKey;
            let nameUrl = BaseUrl + 'getFormName?formKey=' + formKey;

            var schema = null;
            var actionLink = '';
            var name = '';

            axios.get(schemaUrl).then(resp => {
                schema = resp.data;
                axios.get(actionUrl).then(resp => {
                    actionLink = resp.data;
                    axios.get(nameUrl).then(resp => {
                        name = resp.data;

                        commit('set_form_information', { schema, actionLink, name })
                        resolve(resp);
                    }).catch(err => {
                        console.log(err);
                        reject(err)
                    })
                }).catch(err => {
                    console.log(err);
                    reject(err)
                })

            }).catch(err => {
                console.log(err);
                reject(err)
            })

        })
    },

    async fetchFormToEdit({ commit }, formKey) {
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
        console.log(formData);
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
    set_form_information(state, formData) {
        state.formSchema = JSON.parse(formData.schema);
        state.formName = JSON.parse(formData.name)[0].FormName
        state.formActionLink = JSON.parse(formData.actionLink)[0].ActionLink;
    },
    set_forms(state, forms) {
        state.forms = JSON.parse(forms);
    },
    set_form(state, form) {
        state.form = JSON.parse(form);
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