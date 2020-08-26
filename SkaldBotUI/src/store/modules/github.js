import axios from 'axios'
import { BaseGithubUrl, OauthPersonalToken, AcceptMediaType } from '../../helpers/constants'

const state = {
    projects: [],
    projectColumns: [],
    columnCards: [],
    cardInfo: []
}

const getters = {
    getProjects: state => state.projects,
    getProjectColumns: state => state.projectColumns,
    getColumnCards: state => state.columnCards,
    getCardInfo: state => state.cardInfo
}

const actions = {
    async getProjects({ commit }) {
        return new Promise((resolve, reject) => {
            let url = BaseGithubUrl + `repos/The1CABAL/SkaldBot/projects`;
            axios.get(url, {
                headers: {
                    Authorization: 'Bearer ' + OauthPersonalToken,
                    Accept: AcceptMediaType
                }
            }).then(resp => {
                commit('set_projects', resp.data)
                resolve(resp)
            }).catch(err => {
                alert(err)
                reject(err)
            })
        })
    },
    async getProjectColumns({ commit }, projectId) {
        return new Promise((resolve, reject) => {
            let url = BaseGithubUrl + `projects/${projectId}/columns`;
            axios.get(url, {
                headers: {
                    Authorization: 'Bearer ' + OauthPersonalToken,
                    Accept: AcceptMediaType
                }
            }).then(resp => {
                commit('set_project_columns', resp.data)
                resolve(resp)
            }).catch(err => {
                alert(err)
                reject(err)
            })
        })
    },
    async getProjectCardsByColumn({ commit }, columnId) {
        return new Promise((resolve, reject) => {
            let url = BaseGithubUrl + `projects/columns/${columnId}/cards`;
            axios.get(url, {
                headers: {
                    Authorization: 'Bearer ' + OauthPersonalToken,
                    Accept: AcceptMediaType
                }
            }).then(resp => {
                commit('set_column_cards', resp.data)
                resolve(resp)
            }).catch(err => {
                alert(err)
                reject(err)
            })
        })
    },
    async getCardById({ commit }, cardUrl) {
        return new Promise((resolve, reject) => {
            axios.get(cardUrl, {
                headers: {
                    Authorization: 'bearer ' + OauthPersonalToken,
                    Accept: AcceptMediaType
                }
            }).then(resp => {
                commit('set_card_info', resp.data)
                resolve(resp)
            }).catch(err => {
                alert(err)
                reject(err)
            })
        })
    }
}

const mutations = {
    set_projects(state, projects) {
        var passedProjects = projects;

        passedProjects.forEach(obj => {
            Object.entries(obj).forEach(([key, value]) => {
                if (key == "name" && value == "Skald-Bot Kanban") {
                    state.projects = obj;
                }
            })
        })
    },
    set_project_columns(state, projectColumns) {
        state.projectColumns = projectColumns
    },
    set_column_cards(state, columnCards) {
        state.columnCards = columnCards
    },
    set_card_info(state, cardInfo) {
        state.cardInfo = cardInfo
    }
}

export default {
    state,
    getters,
    actions,
    mutations
}