<template>
    <div id="dashboard">
        <div class="sidenav">
            <ul>
                <li><router-link to="/dashboardhome">Dashboard Home</router-link></li>
                <li><router-link to="/manageusers">Users</router-link></li>
                <li><router-link to="/pendingitems">Pending Items</router-link></li>
                <li><router-link to="/managedocumentation">Manage Help</router-link></li>
                <li><router-link to="/manageforms">Manage Forms</router-link></li>
                <li><router-link to="/managestories">Manage Stories</router-link></li>
                <li><router-link to="/managewisdoms">Manage Wisdoms</router-link></li>
                <li><router-link to="/github">GitHub Project</router-link></li>
            </ul>
        </div>
        <div class="dashboardContainer">
            <router-view></router-view>
        </div>
    </div>
</template>

<script>
    export default {
        name: "Dashboard",
        data() {
            return {
                isLoaded: false
            }
        }
    }
</script>

<style scoped>
</style>