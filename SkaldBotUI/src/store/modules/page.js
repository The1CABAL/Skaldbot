const state = {
    loading: true
}

const getters = {
    isReady: state => state.loading === true
}

const actions = {
    async setPageLoading({ commit }) {
        return new Promise((resolve, reject) => {
            commit('page_state', true);
        })
    },
    async setPageLoaded({ commit }) {
        return new Promise((resolve, reject) => {
            commit('page_state', false)
        })
    }
}

const mutations = {
    page_state(state, loading) {
        state.loading = loading;
    }
}

export default {
    state,
    getters,
    actions,
    mutations
}