<template>
    <div id="dashboard">
        <div class="sidenav">
            <ul>
                <li><router-link to="/dashboardhome">Dashboard Home</router-link></li>
                <li><router-link to="/manageusers">Users</router-link></li>
                <li><router-link to="/manageforms">Manage Forms</router-link></li>
                <li><router-link to="/managestories">Manage Stories</router-link></li>
                <li><router-link to="/managewisdoms">Manage Wisdoms</router-link></li>
            </ul>
        </div>
        <div class="dashboardContainer">
            <router-view></router-view>
        </div>
    </div>
</template>

<script>
    import { mapGetters } from "vuex";

    export default {
        name: "Dashboard",
        created: function () {
            if (!this.$store.getters.isMasterAdmin && !this.$store.getters.isAdmin) {
                this.$router.push('/unauthorized')
            }
            else {
                this.$router.push('/dashboardhome')
            }
        },
        computed: {
            ...mapGetters(["isLoggedIn", "isAdmin", "isMasterAdmin", "isUser"])
        },
    }
</script>

<style scoped>
    .sidenav {
        margin-top: 67px;
        margin-left: 8px;
        height: 100%;
        width: 160px;
        position: absolute;
        z-index: 1;
        top: 0;
        left: 0;
        background-color: #479194;
        overflow-x: hidden;
        padding-top: 20px;
    }

        .sidenav ul {
            padding: 6px 8px 6px 16px;
            text-decoration: none;
            color: white;
            display: block;
            padding: 10px;
            font-size: 16px;
            line-height: normal;
            color: white;
        }

            .sidenav ul li a {
                text-decoration: none;
                color: #fff;
                font-size: 12px;
                text-transform: uppercase;
                display: block;
                height: 60px;
                line-height: 60px;
                cursor: pointer;
                padding: 0 10px;
            }

                .sidenav ul li a:hover {
                    color: #ffffff;
                    background-color: #3D8083;
                }

            .sidenav ul .close {
                display: none;
                text-align: right;
                padding: 10px;
            }

                .sidenav ul .close span {
                    font-size: 40px;
                    display: inline-block;
                    padding: 0 10px;
                    cursor: pointer;
                }

    .dashboardContainer {
        margin-left: 163px;
        margin-top: 5px;
    }

    @media screen and (max-height: 450px) {
        .sidenav {
            padding-top: 15px;
        }

            .sidenav a {
                font-size: 18px;
            }
    }

    @media screen and (max-width: 650px) {
        .sidenav {
            width: 25%;
            margin-top: 67px;
        }

            .sidenav ul li a {
                font-size: 6px;
            }

        .dashboardContainer {
            margin-left: 27%;
            margin-top: 1%;
        }
    }
</style>