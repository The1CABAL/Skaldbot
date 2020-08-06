<template>
    <div id="DashboardHome">
        <p>Welcome to the admin dashboard. Select one of the options in the navigation pane to the left to start managing the application!</p>
    </div>
</template>

<script>
    export default {
        name: "DashboardHome",
        created: function () {
            if (this.$store.getters.isLoggedIn) {
                this.reloadAuthentication();
            }
            else {
                if (!this.$store.getters.isMasterAdmin && !this.$store.getters.isAdmin) {
                    this.$router.push('/unauthorized')
                }
                else {
                    this.isLoaded = true
                }
            }
        },
        methods: {
            reloadAuthentication() {
                this.$store.dispatch('loadRoles').then(() => {
                    if (!this.$store.getters.isMasterAdmin && !this.$store.getters.isAdmin) {
                        this.$router.push('/unauthorized')
                    }
                    else {
                        this.isLoaded = true
                    }
                });
            }
        }
    }
</script>

<style scoped>
</style>