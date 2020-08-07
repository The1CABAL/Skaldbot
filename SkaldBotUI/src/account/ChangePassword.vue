<template>
    <div id="HelpDocumentation">
        <transition name="modal-fade">
            <div class="modal-backdrop">
                <div class="modal" role="dialog" aria-labelledby="modalTitle" aria-describedby="modalDescription">
                    <div>
                        <button type="button" class="btn-close topright" @click="close" aria-label="Close modal">x</button>
                    </div>
                    <header class="modal-header" id="modalTitle">
                        <div>
                            <h4>Change Password</h4>
                        </div>
                    </header>
                    <section class="modal-body" id="modalDescription">
                        <Form :formKey="formKey" :passedModel="model" @PasswordSuccess="success" />
                    </section>
                    <footer class="modal-footer">
                        <div>
                            <slot name="footer">
                                <button type="button" class="btn-button" @click="close">
                                    Close
                                </button>
                            </slot>
                        </div>
                    </footer>
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
        mounted() {
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