<template>
    <div id="Register">
        <Form v-if="formKey != ''" :formKey="formKey" @RegisterSuccess="login" />
        <router-link to="/login" class="link">Login</router-link>
        <button type="button" v-on:click="openHelp" class="btn-button">Help</button>
        <HelpDocumentation v-if="showHelp" :HelpContentKey="helpContentKey" @close="closeHelp"></HelpDocumentation>
    </div>
</template>

<script>
    import Form from '../components/Forms/Form';
    import HelpDocumentation from '../components/HelpDocumentation'
    export default {
        name: 'Register',
        components: {
            Form,
            HelpDocumentation
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
                console.log("Logging in...")
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