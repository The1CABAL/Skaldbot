<template>
    <div id="app" class="bg-primary text-white">
        <div v-if="!loading">
            <nav-bar @logged-out="reloadAuthentication" />
            <header>
                <div class="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8">
                    <h1 class="text-2xl font-bold border-b-2 border-gray-200 pb-2">
                        {{currentPage}}
                    </h1>
                </div>
            </header>
            <main>
                <div class="max-w-7xl mx-auto py-3 sm:px-6 lg:px-8 min-h-screen h-full">
                    <router-view @authenticated="reloadAuthentication" />
                </div>
            </main>

        </div>
    </div>
</template>

<script>
    import navBar from './components/Nav/navBar.vue';
    export default {
        name: "app",
        data() {
            return {
                currentPage: 'Home',
                loading: false
            }
        },

        components: {
            'nav-bar': navBar
        },

        mounted() {
            this.currentPage = this.$route.name.toUpperCase();

            if (this.$store.getters.isLoggedIn) {
                this.reloadAuthentication();
            }
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
        },

        methods: {
            reloadAuthentication() {
                if (!this.$store.getters.isLoggedIn) {
                    return;
                }

                this.loading = true;

                this.$store.dispatch('loadRoles').then(() => {
                    this.loading = false;
                });
            },
        },

        watch: {
            '$route.name' (newVal, oldVal) {
                if (newVal !== oldVal) {
                    this.currentPage = this.$route.name.toUpperCase();
                }
            }
        }
    }
</script>

<style src="@/style/main.css">
</style>