<template>
    <div id="Register">
        <Form v-if="formKey != ''" :formKey="formKey" @RegisterSuccess="login" />
        <div class="space-x-2">
            <router-link to="/login" class="min-w-32 max-w-xs w-auto pr-2 pl-2 mb-2 p-2 h-32 rounded-md text-white bg-secondary hover:bg-hover">Login</router-link>
            <vue-button varient="secondary" type="button" v-on:click="openHelp" class="btn-button">Help</vue-button>
        </div>
        <HelpDocumentation v-if="showHelp" :HelpContentKey="helpContentKey" @close="closeHelp"></HelpDocumentation>
    </div>
</template>

<script>
    import Form from '../components/Forms/Form';
    import HelpDocumentation from '../components/HelpDocumentation'
    import fieldButton from '@/components/CustomFields/fieldButton'
    import PageMixin from '@/mixins/page-mixin'

    export default {
        name: 'Register',

        components: {
            Form,
            HelpDocumentation,
            'vue-button': fieldButton
        },

        mixins: [PageMixin],

        beforeMount() {
            this.pageMounting();
        },

        mounted() {
            this.pageMounted().then(() => {
                this.pageReady();
            })
        },

        data() {
            return {
                formKey: 'RegisterForm',
                helpContentKey: 'RegisterHelp',
                showHelp: false,
            }
        },

        methods: {
            login() {
                this.$emit("authenticated", true)
            },
            openHelp() {
                this.showHelp = true;
            },
            closeHelp() {
                this.showHelp = false;
            }
        }
    }
</script>

<style scoped>
    .link {
        margin-left: 1%;
        display: inline-block;
        color: #444;
        border: 1px solid #CCC;
        background: #DDD;
        box-shadow: 0 0 5px -1px rgba(0,0,0,0.2);
        cursor: pointer;
        vertical-align: middle;
        max-width: 100px;
        padding: 5px;
        text-align: center;
        text-decoration: none;
    }

        .link:hover {
            background: #B8B8B8;
        }
</style>