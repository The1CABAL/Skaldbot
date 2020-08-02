import axios from 'axios';
import { BaseUrl } from '../../helpers/constants';
import JSONbig from 'json-bigint'

const state = {
    submittedResponse: '',
    submittedItem: [],
    story: [],
    wisdom: []
};

const getters = {
    getSubmittedResponse: state => state.submittedResponse,
    getSubmittedItem: state => state.submittedItem,
    getStory: state => state.story,
    getWisdom: state => state.wisdom
};

const actions = {
    async updateSuggestionState({ commit }, suggestionData) {
        let url = BaseUrl + 'submittedItems'
        return new Promise((resolve, reject) => {
            axios.post(url, suggestionData).then(resp => {
                commit('set_submitted_response', resp.data);
                resolve(resp);
            }).catch(err => {
                console.log(err);
                reject(err);
            })
        })
    },
    async updateStory({ commit }, story) {
        let url = BaseUrl + 'story'
        return new Promise((resolve, reject) => {
            axios.post(url, story).then(resp => {
                commit('set_submitted_response', resp.data);
                resolve(resp);
            }).catch(err => {
                console.log(err);
                reject(err);
            })
        })
    },
    async updateWisdom({ commit }, wisdom) {
        let url = BaseUrl + 'wisdom'
        return new Promise((resolve, reject) => {
            axios.post(url, wisdom).then(resp => {
                commit('set_submitted_response', resp.data);
                resolve(resp);
            }).catch(err => {
                console.log(err);
                reject(err);
            })
        })
    },
    async getSubmittedItemData({ commit }, lookupId) {
        let url = BaseUrl + 'submititem?id=' + lookupId
        return new Promise((resolve, reject) => {
            axios.get(url).then(resp => {
                commit('set_submitted_item', resp.data);
                resolve(resp);
            }).catch(err => {
                console.log(err);
                reject(err);
            })
        })
    },
    async getStoryData({ commit }, storyId) {
        let url = BaseUrl + 'story?id=' + storyId
        return new Promise((resolve, reject) => {
            axios.get(url).then(resp => {
                commit('set_story', resp.data)
                resolve(resp);
            }).catch(err => {
                console.log(err);
                reject(err);
            })
        })
    },
    async getWisdomData({ commit }, wisdomId) {
        let url = BaseUrl + 'wisdom?id=' + wisdomId
        return new Promise((resolve, reject) => {
            axios.get(url).then(resp => {
                commit('set_wisdom', resp.data);
                resolve(resp);
            }).catch(err => {
                console.log(err);
                reject(err);
            })
        })
    }
};

const mutations = {
    set_submitted_response(state, response) {
        state.submittedResponse = response.Message.toString();
    },
    set_submitted_item(state, submittedItem) {
        state.submittedItem = JSON.parse(submittedItem)
    },
    set_story(state, story) {
        state.story = JSONbig.parse(story)
    },
    set_wisdom(state, wisdom) {
        state.wisdom = JSONbig.parse(wisdom)
    }
};

export default {
    state,
    getters,
    actions,
    mutations
}