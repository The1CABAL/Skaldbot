<template>
    <div id="RegisterUser">
        <button type="button" class="btn-button" v-on:click="goBack">Go Back</button>
        <Form :formKey="formKey" :accountId="accountId" @RegisterSuccess="alert" />
        <button type="button" v-on:click="openHelp" class="btn-button">Help</button>
        <HelpDocumentation v-if="showHelp" :HelpContentKey="helpContentKey" @close="closeHelp"></HelpDocumentation>
    </div>
</template>

<script>
    import Form from '../../components/Forms/Form';
    import HelpDocumentation from '../../components/HelpDocumentation'
    export default {
        name: 'RegisterUser',
        props: {
            accountId: {
                type: String,
                required: true
            }
        },
        components: {
            Form,
            HelpDocumentation
        },
        beforeRouteEnter(to, from, next) {
            next((vm) => {
                vm.prevRoute = from
            })
        },
        data() {
            return {
                formKey: 'RegisterUserForm',
                helpContentKey: 'RegisterHelp',
                showHelp: false,
            }
        },
        methods: {
            alert() {
                this.$emit('registerUserSuccess', true)
            },
            goBack() {
                this.$router.push(this.prevRoute.path)
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