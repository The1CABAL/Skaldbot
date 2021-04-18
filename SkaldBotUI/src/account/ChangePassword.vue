<template>
    <div id="HelpDocumentation">
        <transition name="modal-fade">
            <div class="modal-backdrop">
                <div class="modal" role="dialog" aria-labelledby="modalTitle" aria-describedby="modalDescription">
                    <section class="modal-body" id="modalDescription">
                        <Form :formKey="formKey" :passedModel="model" @PasswordSuccess="success" @close="close" showCloseButton/>
                    </section>
                </div>
            </div>
        </transition>
    </div>
</template>

<script>
    import VueLoading from '../components/VueLoading';
    
    import Form from '../components/Forms/Form';

    export default {
        name: "HelpDocumentation",
        components: {
            VueLoading,
            Form
        },
        data() {
            return {
                isAdmin: false,
                formKey: 'UpdatePassword',
                model: []
            }
        },
        created() {
            this.reloadAuthentication();
            this.getData();
        },
        beforeDestroy() {
        },
        methods: {
            getData() {
                var defaultModel = {
                    UserId: this.$store.getters.userId
                }
                var populatedModel = [defaultModel]
                this.model = populatedModel;
            },
            close() {
                this.$emit('close');
            },
            reloadAuthentication() {
                this.$store.dispatch('loadRoles').then(() => {
                    if (this.$store.getters.isMasterAdmin || this.$store.getters.isAdmin) {
                        this.isAdmin = true;
                    }
                });
            }
        }
    }
</script>

<style scoped>
</style>