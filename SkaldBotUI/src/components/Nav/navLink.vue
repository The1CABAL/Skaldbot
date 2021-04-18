<template>
    <div>
        <router-link class="text-white px-3 py-2 rounded-md text-sm font-medium hover:bg-hover" v-if="!dropdownLink && !mobile" :to="to" v-on:click.native="onClick"><slot></slot></router-link>
        <router-link class="text-white hover:bg-hover hover:text-white block px-3 py-2 rounded-md text-base font-medium" v-if="!dropdownLink && mobile" :to="to" v-on:click.native="onClick"><slot></slot></router-link>
        <router-link class="block px-4 py-2 text-sm text-gray-700 hover:bg-hover" :to="to" v-if="dropdownLink && !mobile" v-on:click.native="onClick"><slot></slot></router-link>
        <router-link class="block px-3 py-2 rounded-md text-base font-medium text-white hover:text-white hover:bg-hover" :to="to" v-if="dropdownLink && mobile" v-on:click.native="onClick"><slot></slot></router-link>
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
            }
        },

        methods: {
            onClick() {
                this.$emit('click');
            }
        }
    }
</script>