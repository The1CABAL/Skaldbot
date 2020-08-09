<template>
    <div id="app">
        <div class="container-nav">
            <div class="logo">
                <router-link to="/"><img :src="logoImage" style="height: 60px;" /></router-link>
            </div>
            <div class="navbar">
                <div class="icon-bar" @click="Show()">
                    <i></i>
                    <i></i>
                    <i></i>
                </div>
                <ul id="nav-lists">
                    <li class="close"><span @click="Hide()">&times;</span></li>
                    <li><router-link to="/" v-on:click.native="Hide()">Home</router-link></li>
                    <li><router-link to="/about" v-on:click.native="Hide()">About</router-link></li>
                    <li><router-link to="/suggestions" v-on:click.native="Hide()">Submit Ideas</router-link></li>
                    <li><router-link to="/dashboard" v-if="authenticated && (admin || masterAdmin)" v-on:click.native="Hide()">Dashboard</router-link></li>
                    <li><router-link to="/accountprofile" v-if="authenticated && clientAdmin" v-on:click.native="account(); Hide()">Account Profile</router-link></li>
                    <li><router-link to="/userprofile" v-if="authenticated" v-on:click.native="profile(); Hide()">User Profile</router-link></li>
                    <li><router-link to="/manageserver" v-if="authenticated" v-on:click.native="Hide()">Manage Channels</router-link></li>
                    <li><router-link to="/" v-if="authenticated" v-on:click.native="logout(); Hide()">Logout</router-link></li>
                    <li><router-link to="login" v-if="!authenticated" v-on:click.native="Hide()">Login</router-link></li>
                </ul>
            </div>
        </div>
        <router-view @authenticated="setAuthenticated"></router-view>
    </div>
</template>

<script>
    import { mapGetters } from "vuex";
    export default {
        name: "app",
        data() {
            return {
                authenticated: false,
                logoImage: require('@/assets/logo.png'),
                background: require('@/assets/SbBackground.jpg'),
                masterAdmin: false,
                clientAdmin: false,
                admin: false,
                user: true,
                userActivityThrottlerTimeout: null,
                userActivityTimeout: null,
            }
        },
        beforeMount() {
            this.activateActivityTracker();
        },
        beforeDestroy() {
            window.removeEventListener("mousemove", this.userActivityThrottler);
            window.removeEventListener("scroll", this.userActivityThrottler);
            window.removeEventListener("keydown", this.userActivityThrottler);
            window.removeEventListener("resize", this.userActivityThrottler);

            clearTimeout(this.userActivityTimeout);
            clearTimeout(this.userActivityThrottlerTimeout);
        },
        mounted() {
            if (this.$store.getters.isLoggedIn) {
                this.reloadAuthentication();
            }
        },
        watch: {
        },
        computed: {
            ...mapGetters(["isLoggedIn", "isAdmin", "isMasterAdmin", "isUser"])
        },
        created: function () {
            this.$http.interceptors.response.use(undefined, function (err) {
                return new Promise(function (resolve, reject) {
                    if (err.status == 401 && err.config && !err.config__isRetryRequest) {
                        this.$store.dispatch(logout)
                    }
                    throw err;
                });
            });

            if (this.$store.getters.isLoggedIn) {
                this.reloadAuthentication();
            }
        },
        methods: {
            Show() {
                document.getElementById("nav-lists").classList.add("_Menus-show");
            },
            Hide() {
                document.getElementById("nav-lists").classList.remove("_Menus-show");
            },
            setAuthenticated() {
                var url = this.$route.path;

                if (url == '/login' || url == '/register') {
                    this.$router.push('/')
                    this.$store.dispatch('loadRoles').then(() => {
                        if (this.$store.getters.isMasterAdmin) {
                            this.masterAdmin = true;
                            this.admin = true;
                            this.clientAdmin = true;
                        }
                        else if (this.$store.getters.isAdmin) {
                            this.admin = true;
                            this.clientAdmin = true;
                        }
                        else if (this.$store.getters.isClientAdmin) {
                            this.clientAdmin = true;
                        }

                        this.authenticated = true;
                        this.$message("Successfully Signed In!");
                    }).catch(err => console.log(err));
                }
                else {
                    this.$store.dispatch('loadRoles').then(() => {
                        if (this.$store.getters.isMasterAdmin) {
                            this.masterAdmin = true;
                            this.admin = true;
                            this.clientAdmin = true;
                        }
                        else if (this.$store.getters.isAdmin) {
                            this.admin = true;
                            this.clientAdmin = true;
                        }
                        else if (this.$store.getters.isClientAdmin) {
                            this.clientAdmin = true;
                        }

                        this.authenticated = true;
                    });
                }
            },
            logout() {
                this.$store.dispatch('logout').then(() => {
                    this.authenticated = false;
                    this.masterAdmin = false;
                    this.admin = false;
                    this.clientAdmin = false;
                    this.$message("Logged out!")
                })

            },
            activateActivityTracker() {
                window.addEventListener("mousemove", this.userActivityThrottler);
                window.addEventListener("mousemove", this.resetUserActivityTimeout);
                window.addEventListener("scroll", this.resetUserActivityTimeout);
                window.addEventListener("keydown", this.resetUserActivityTimeout);
                window.addEventListener("resize", this.resetUserActivityTimeout);
            },
            resetUserActivityTimeout() {
                clearTimeout(this.userActivityTimeout);
                this.userActivityTimeout = setTimeout(() => {
                    this.inactiveUserAction();
                }, 1800000);
            },
            userActivityThrottler() {
                if (!this.userActivityThrottlerTimeout) {
                    this.userActivityThrottlerTimeout = setTimeout(() => {
                        this.resetUserActivityTimeout();

                        clearTimeout(this.userActivityThrottlerTimeout);
                        this.userActivityThrottlerTimeout = null;
                    }, 1800000);
                }
            },
            inactiveUserAction() {
                if (this.authenticated) {
                    this.$store.dispatch('logout')
                    location.reload();
                }
            },
            reloadAuthentication() {
                this.$store.dispatch('loadRoles').then(() => {
                    if (this.$store.getters.isMasterAdmin) {
                        this.masterAdmin = true;
                        this.admin = true;
                        this.clientAdmin = true;
                    }
                    else if (this.$store.getters.isAdmin) {
                        this.admin = true;
                        this.clientAdmin = true;
                    }
                    else if (this.$store.getters.isClientAdmin) {
                        this.clientAdmin = true;
                    }
                    this.authenticated = true;
                });
            },
            profile() {
                this.$router.push('/userprofile/' + this.$store.getters.userId)
            },
            account() {
                this.$router.push('/accountprofile/' + this.$store.getters.getAccountId);
            }
        }
    }
</script>

<style src="@/style/main.css">
</style>