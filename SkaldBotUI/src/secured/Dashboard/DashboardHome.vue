<template>
    <div id="DashboardHome">
        <p>This is the home dashboard</p>
    </div>
</template>

<script>
    export default {
        name: "DashboardHome",
        created: function () {
            if (!this.$store.getters.isMasterAdmin && !this.$store.getters.isAdmin) {
                this.$router.push('/unauthorized')
            }
            else {
                this.isLoaded = true
            }
        }
    }
</script>

<style scoped>
</style>