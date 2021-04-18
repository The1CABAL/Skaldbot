<template>
    <nav class="bg-primary shadow-lg">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex items-center justify-between h-16">
                <div class="flex items-center">
                    <div class="flex-shrink-0" @click="$router.push('/')">
                        <img class="h-15 w-20" :src="logoImage" alt="Workflow">
                    </div>
                    <div class="hidden md:block">
                        <div class="ml-10 flex items-baseline space-x-4">
                            <nav-link to="/">Home</nav-link>
                            <nav-link to="/about">About</nav-link>
                            <nav-link to="/suggestions">Submit Ideas</nav-link>
                            <nav-link to="/dashboard" v-if="authenticated && (admin || masterAdmin)">Dashboard</nav-link>
                            <nav-link to="/login" v-if="!authenticated">Login</nav-link>
                        </div>
                    </div>
                </div>
                <div class="hidden md:block" v-if="authenticated">
                    <div class="ml-4 flex items-center md:ml-6">
                        <!-- Profile dropdown -->
                        <div class="ml-3 relative">
                            <div>
                                <button type="button" class="max-w-xs bg-gray-800 rounded-full flex items-center text-sm focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-800 focus:ring-white" id="user-menu-button" aria-expanded="false" aria-haspopup="true" @click="toggleProfileDropdown">
                                    <span class="sr-only">Open user menu</span>
                                    <div class="h8 w-8 rounded-full">
                                        <div v-html="avatarUrl"></div>
                                    </div>
                                </button>
                            </div>
                            <div v-if="profileDropdown" class="origin-top-right absolute right-0 mt-2 w-48 rounded-md shadow-lg py-1 bg-white ring-1 ring-black ring-opacity-5 focus:outline-none z-50" role="menu" aria-orientation="vertical" aria-labelledby="user-menu-button" tabindex="-1">
                                <nav-link dropdownLink to="/accountprofile" v-if="clientAdmin" v-on:click.native="account(); toggleProfileDropdown()">Account Profile</nav-link>
                                <nav-link dropdownLink to="/userprofile" v-on:click.native="profile(); toggleProfileDropdown()">User Profile</nav-link>
                                <nav-link dropdownLink to="/manageserver" v-on:click.native="toggleProfileDropdown()">Manage Channels</nav-link>
                                <nav-link dropdownLink to="/" v-on:click.native="logout(); toggleProfileDropdown()">Logout</nav-link>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="-mr-2 flex md:hidden">
                    <!-- Mobile menu button -->
                    <button type="button" class="bg-gray-800 inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-white hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-800 focus:ring-white" aria-controls="mobile-menu" aria-expanded="false" @click="toggleMobileNav">
                        <span class="sr-only">Open main menu</span>
                        <svg class="block h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
                        </svg>
                        <svg class="hidden h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                </div>
            </div>
        </div>

        <!-- Mobile menu, show/hide based on menu state. -->
        <div class="md:hidden" id="mobile-menu" v-if="showMobileNav">
            <div class="px-2 pt-2 pb-3 space-y-1 sm:px-3">
                <nav-link mobile to="/" v-on:click.native="toggleMobileNav()">Home</nav-link>
                <nav-link mobile to="/about" v-on:click.native="toggleMobileNav()">About</nav-link>
                <nav-link mobile to="/suggestions" v-on:click.native="toggleMobileNav()">Submit Ideas</nav-link>
                <nav-link mobile to="/dashboard" v-if="authenticated && (admin || masterAdmin)" v-on:click.native="toggleMobileNav()">Dashboard</nav-link>
                <nav-link mobile to="/login" v-if="!authenticated" v-on:click.native="toggleMobileNav()">Login</nav-link>
            </div>
            <div class="pt-4 pb-3 border-t border-gray-700" v-if="authenticated">
                <div class="flex items-center">
                    <div class="h8 w-8 rounded-full ml-3">
                        <div v-html="avatarUrl"></div>
                    </div>
                    <div class="ml-3">
                        <div class="text-base font-medium leading-none text-white">Tom Cook</div>
                    </div>
                </div>
                <div class="mt-3 px-2 space-y-1">
                    <nav-link dropdownLink mobile to="/accountprofile" v-if="clientAdmin" v-on:click.native="account(); toggleMobileNav()">Account Profile</nav-link>
                    <nav-link dropdownLink mobile to="/userprofile" v-on:click.native="profile(); toggleMobileNav()">User Profile</nav-link>
                    <nav-link dropdownLink mobile to="/manageserver" v-on:click.native="toggleMobileNav()">Manage Channels</nav-link>
                    <nav-link dropdownLink mobile to="/" v-on:click.native="logout(); toggleMobileNav()">Logout</nav-link>
                </div>
            </div>
        </div>
    </nav>
</template>

<script>
    import navLink from './navLink.vue';
    import multiavatar from '@multiavatar/multiavatar'
    import PageMixin from '@/mixins/page-mixin'

    export default {
        components: {
            'nav-link': navLink
        },

        mixins: [PageMixin],

        data() {
            return {
                profileDropdown: false,
                showMobileNav: false,
                logoImage: require('@/assets/logo.png'),
            }
        },

        computed: {
            avatarUrl() {
                return multiavatar('Binx Bond')
            }
        },

        methods: {
            toggleProfileDropdown() {
                this.profileDropdown = !this.profileDropdown;
            },

            toggleMobileNav() {
                this.showMobileNav = !this.showMobileNav;
            },

            profile() {
                this.$router.push('/userprofile/' + this.$store.getters.userId)
            },

            account() {
                this.$router.push('/accountprofile/' + this.$store.getters.getAccountId);
            },

            logout() {
                this.$store.dispatch('logout').then(() => {
                    this.$emit('logged-out');
                })
            },
        }
        
    }
</script>