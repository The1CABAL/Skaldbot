<template>
    <div>
        <router-link class="text-white px-3 py-2 rounded-md text-sm font-medium hover:bg-hover" v-if="notMobileOrDropdown" :to="to" v-on:click.native="onClick"><slot></slot></router-link>

        <router-link class="text-white hover:bg-hover hover:text-white block px-3 py-2 rounded-md text-base font-medium" v-if="mobileNotDropdown" :to="to" v-on:click.native="onClick"><slot></slot></router-link>

        <router-link class="block px-4 py-2 text-sm text-gray-700 hover:bg-hover" :to="to" v-if="notMobileDropdown" v-on:click.native="onClick"><slot></slot></router-link>

        <router-link class="block px-3 py-2 rounded-md text-base font-medium text-white hover:text-white hover:bg-hover" :to="to" v-if="mobileDropdown" v-on:click.native="onClick"><slot></slot></router-link>

        <router-link class="border-transparent text-white hover:bg-hover group flex items-center px-3 py-2 text-sm font-medium border-l-4 rounded-md" :to="to" v-if="sideNavLink" v-on:click.navtive="onClick"><slot></slot></router-link>
    </div>
</template>

<script>
    export default {
        props: {
            to: {
                type: String,
                required: true
            },
            dropdownLink: {
                type: Boolean,
                required: false,
                default: false
            },
            mobile: {
                type: Boolean,
                required: false,
                default: false
            },
            sideNavLink: {
                type: Boolean,
                default: false
            }
        },

        methods: {
            onClick() {
                this.$emit('click');
            }
        },

        computed: {
            notMobileOrDropdown() {
                return !this.dropdownLink && !this.mobile && !this.sideNavLink
            },

            mobileNotDropdown() {
                return !this.dropdownLink && this.mobile && !this.sideNavLink
            },

            notMobileDropdown() {
                return this.dropdownLink && !this.mobile && !this.sideNavLink
            },

            mobileDropdown() {
                return this.dropdownLink && this.mobile && !this.sideNavLink
            },

            sideLink() {
                return !this.dropdownLink && !this.mobile && this.sideNavLink
            }
        }
    }
</script>