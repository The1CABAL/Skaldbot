export default {
    data() {
        return {
            prevRoute: {}
        }
    },

    beforeRouteEnter(to, from, next) {
        next((vm) => {
            vm.prevRoute = from
        })
    },

    methods: {
        pageMounting() {
            this.$store.dispatch('setPageLoading');
        },

        async pageMounted() {
            if (this.$store.getters.isLoggedIn) {
                await this.reloadRoles();
            }
        },

        async reloadRoles() {
            await this.$store.dispatch('loadRoles');
        },

        pageReady() {
            this.$store.dispatch('setPageLoaded');
        },

        redirectUser(endpoint, endpointParams) {
            if (endpointParams) {
                let obj = { path: endpoint, params: { ...endpointParams } }
                this.$router.push(obj);
                return;
            }

            this.$router.push({ path: endpoint });
        },

        goBack() {
            if (this.prevRoute.path === undefined || this.prevRoute.path === this.$route.path) {
                this.redirectUser('/');
                return;
            }

            this.redirectUser(this.prevRoute.path);
        },

        success(message, title) {
            const notification = {
                type: 'Success',
                title: title || 'Success!',
                message: message
            }

            this.addNotification(notification);
        },

        warning(message, title) {
            const notification = {
                type: 'Warning',
                title: title || 'Warning!',
                message: message
            }

            this.addNotification(notification);
        },

        error(message, title) {
            const notification = {
                type: 'Error',
                title: title || 'Error!',
                message: message
            }

            this.addNotification(notification);
        },

        addNotification(notification) {
            this.$store.dispatch('addNotification', notification)

            let currentNotification = this.$store.getters.currentNotification;

            setTimeout(() => {
                this.$store.dispatch('removeNotification', currentNotification);
            }, 5000)
        }
    },

    computed: {
        masterAdmin() {
            return this.$store.getters.isMasterAdmin
        },

        clientAdmin() {
            return this.$store.getters.isClientAdmin || this.masterAdmin || this.admin;
        },

        admin() {
            return this.$store.getters.isAdmin || this.masterAdmin;
        },

        authenticated() {
            return this.$store.getters.isLoggedIn;
        }
    }
}