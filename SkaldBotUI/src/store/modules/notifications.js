const state = {
    notifications: []
}

const getters = {
    currentNotification: state => state.notifications[state.notifications.length - 1] || null,
    getNotifications: state => state.notification
}

const actions = {
    async addNotification({ commit }, notification) {
        return new Promise((resolve, reject) => {
            commit('add_notification', notification);
            resolve();
        })
    },

    async removeNotification({ commit }, notification) {
        return new Promise((resolve, reject) => {
            commit('remove_notification', notification);
            resolve();
        })
    }
}

const mutations = {
    add_notification(state, notification) {
        const id = state.notifications.length > 0 ? state.notifications[state.notifications.length - 1].id + 1 : 1;
        let { type, title, message } = notification;
        state.notifications.push({ id: id, title: title, type: type, message: message })
    },

    remove_notification(state, notification) {
        state.notifications = state.notifications.filter(function (n) { return n.id != notification.id; }); 
    }
}

export default {
    state,
    getters,
    actions,
    mutations
}