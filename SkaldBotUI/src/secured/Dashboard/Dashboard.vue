<template>
    <div class="h-screen flex overflow-hidden bg-primary">
        <div class="fixed inset-0 flex z-40 lg:hidden" role="dialog" aria-modal="true" v-if="mobileNav">
            <div class="fixed inset-0 bg-primary bg-opacity-75" aria-hidden="true"></div>
            <div class="relative flex-1 flex flex-col max-w-xs w-full bg-primary focus:outline-none">
                <div class="absolute top-0 right-0 -mr-12 pt-2">
                    <button type="button" class="ml-1 flex items-center justify-center h-10 w-10 rounded-full focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white" @click="toggleMobileNav">
                        <span class="sr-only">Close sidebar</span>
                        <svg class="h-6 w-6 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                </div>

                <div class="flex-1 h-0 pb-4 overflow-y-auto">
                    <side-nav @sideNavClick="toggleMobileNav"/>
                </div>
            </div>
            <div class="flex-shrink-0 w-14" aria-hidden="true">
            </div>
        </div>
        <div class="hidden lg:flex lg:flex-shrink-0">
            <div class="flex flex-col w-64">
                <side-nav @sideNavClick="toggleMobileNav" />
            </div>
        </div>
        <div class="flex flex-col min-w-0 flex-1 overflow-hidden">
            <div class="lg:hidden">
                <div class="flex items-center justify-between bg-primary border-b border-gray-200 px-4 py-1.5">
                    <div>
                        <button type="button" class="-mr-3 h-12 w-12 inline-flex items-center justify-center rounded-md text-white hover:text-gray-300" @click="toggleMobileNav">
                            <span class="sr-only">Open sidebar</span>
                            <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
                            </svg>
                        </button>
                    </div>
                </div>
            </div>
            <div class="flex-1 relative z-0 flex overflow-hidden">
                <main class="flex-1 relative z-0 overflow-y-auto focus:outline-none xl:order-last">
                    <!-- Start main area-->
                    <div class="absolute inset-0 py-6 px-4 sm:px-6 lg:px-8">
                        <div class="h-full border-2 rounded-lg p-5 panel">
                            <router-view />
                        </div>
                    </div>
                    <!-- End main area -->
                </main>
            </div>
        </div>
    </div>
</template>

<script>
    import sideNavBar from '@/components/Nav/sideNavBar';
    import PageMixin from '@/mixins/page-mixin';

    export default {
        name: "Dashboard",

        data() {
            return {
                mobileNav: false
            }
        },

        mixins: [PageMixin],

        components: {
            'side-nav': sideNavBar
        },

        beforeMount() {
            this.pageMounting();
        },

        mounted() {
            this.pageMounted().then(() => {
                if (!this.masterAdmin || !this.admin) {
                    this.redirectUser('/unauthorized')
                    this.pageReady();
                }
            })
        },

        methods: {
            toggleMobileNav() {
                this.mobileNav = !this.mobileNav;
            }
        }
    }
</script>
