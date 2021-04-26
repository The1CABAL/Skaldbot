import axios from 'axios'
import { BaseGithubUrl, OauthPersonalToken, AcceptMediaType } from '../../helpers/constants'


const state = {
    msg: '',
    projects: [],
    projectColumns: [],
    columnCards: [],
    cardInfo: [],
    cardComments: []
}

const getters = {
    getGitHubUpdateMsg: state => state.msg,
    getProjects: state => state.projects,
    getProjectColumns: state => state.projectColumns,
    getColumnCards: state => state.columnCards,
    getCardInfo: state => state.cardInfo,
    getCardComments: state => state.cardComments
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
                console.log(err)
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
                console.log(err)
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
                console.log(err)
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
                console.log(err)
                reject(err)
            })
        })
    },
    async getAllCardComments({ commit }, commentUrl) {
        return new Promise((resolve, reject) => {
            axios.get(commentUrl, {
                headers: {
                    Authorization: 'bearer ' + OauthPersonalToken,
                    Accept: AcceptMediaType
                }
            }).then(resp => {
                commit('set_card_comments', resp.data)
                resolve(resp)
            }).catch(err => {
                console.log(err)
                reject(err)
            })
        })
    },
    async updateProjectIssue({ commit }, projectIssue) {
        let url = projectIssue.url;
        let issue = projectIssue.updatedCardInfo;
        console.log(url);
        return new Promise((resolve, reject) => {
            axios({
                method: 'patch',
                url: url,
                headers: {
                    Authorization: 'bearer ' + OauthPersonalToken,
                    Accept: AcceptMediaType,
                },
                data: {
                    title: issue.title,
                    body: issue.body,
                    state: issue.state,
                    milestone: issue.milestone,
                    labels: issue.labels,
                    assignees: issue.assignees
                }
            }).then(resp => {
                commit('set_update_issue', resp.data)
                resolve(resp)
            }).catch(err => {
                commit('set_fail_update_issue')
                console.log(err)
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
        state.projectColumns = projectColumns;
    },
    set_column_cards(state, columnCards) {
        state.columnCards = columnCards;
    },
    set_card_info(state, cardInfo) {
        state.cardInfo = cardInfo;
    },
    set_card_comments(state, cardComments) {
        state.cardComments = cardComments;
    },
    set_update_issue(state, updatedIssue) {
        state.cardInfo = updatedIssue;
        state.msg = 'Success';
    },
    set_fail_update_issue(state) {
        state.msg = 'Fail'
    }
}

export default {
    state,
    getters,
    actions,
    mutations
}