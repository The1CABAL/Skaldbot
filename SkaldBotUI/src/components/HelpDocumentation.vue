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
                            <h4 v-if="!isLoaded"></h4>
                            <br />
                            <h4 v-if="(isLoaded && !isAdmin) || (isLoaded && isAdmin && userView)">{{helpTitle}}</h4>
                            <label for="helpTitle" v-if="isAdmin && !userView">Title:</label>
                            <input type="text" name="helpTitle" v-model="helpTitle" v-if="isAdmin && !userView" />
                        </div>
                    </header>
                    <section class="modal-body" id="modalDescription">
                        <button type="button" class="btn-button" v-if="isAdmin" v-on:click="userDisplay">Toggle Edit</button>
                        <vue-editor v-model="helpContent" v-if="isLoaded && isAdmin && !userView"></vue-editor>
                        <p v-if="(isLoaded && !isAdmin) || (isLoaded && isAdmin && userView)"><span v-html="helpContent"></span></p>
                        <VueLoading v-if="!isLoaded"></VueLoading>
                    </section>
                    <footer class="modal-footer">
                        <div>
                            <slot name="footer">
                                <button type="button" class="btn-button approve" @click="saveContent" v-if="isAdmin && !userView">
                                    Save
                                </button>
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
    import { VueEditor } from "vue2-editor";
    import VueLoading from '../components/VueLoading';

    export default {
        name: "HelpDocumentation",
        components: {
            VueEditor,
            VueLoading
        },
        props: {
            HelpContentKey: {
                type: String,
                required: true
            }
        },
        data() {
            return {
                isLoaded: false,
                isAdmin: false,
                userView: true,
                helpTitle: '',
                helpContent: '',
                isActive: true
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
                var key = this.HelpContentKey;
                var admin = this.isAdmin;
                var docInfo = { "HelpContentKey": key, "IsAdmin": admin }
                this.$store.dispatch('getDocumentation', docInfo).then(() => {
                    this.helpContent = this.$store.getters.helpContent;
                    this.helpTitle = this.$store.getters.helpTitle;
                    this.isActive = this.$store.getters.helpIsActive;
                    this.isLoaded = true;
                }).catch((err) => {
                    console.log(err)
                    this.$message("Error getting documentation")
                })
            },
            close() {
                this.$emit('close');
            },
            saveContent: function () {
                // You have the content to save
                this.isLoaded = false;

                var helpContentKey = this.HelpContentKey;
                var helpTitle = this.helpTitle;
                var helpContent = this.helpContent;
                var isActive = this.isActive;
                var userId = this.$store.getters.userId;
                var isAdmin = this.isAdmin;

                this.$store.dispatch('updateDocumentation', { helpContentKey, helpTitle, helpContent, isActive, userId, isAdmin }).then(() => {
                    this.helpContent = this.$store.getters.helpContent;
                    this.helpTitle = this.$store.getters.helpTitle;
                    this.isActive = this.$store.getters.helpIsActive;
                    this.isLoaded = true;
                    this.$message("Content updated")
                }).catch((err) => {
                    console.log(err);
                    this.$message("Error updating content");
                })
            },
            reloadAuthentication() {
                this.$store.dispatch('loadRoles').then(() => {
                    if (this.$store.getters.isMasterAdmin || this.$store.getters.isAdmin) {
                        this.isAdmin = true;
                        this.userView = false;
                    }
                });
            },
            userDisplay() {
                if (this.userView)
                    this.userView = false;
                else
                    this.userView = true;
            }
        }
    }
</script>

<style scoped>
</style>