<template>
    <div id="HelpDocumentation">
        <div class="fixed z-10 inset-0 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
            <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
                <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" aria-hidden="true"></div>
                <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
                <div class="inline-block align-bottom bg-primary rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-3xl sm:w-full sm:p-6">
                    <div>
                        <vue-button type="button" varient="secondary" v-if="admin" v-on:click="userDisplay">Toggle Edit</vue-button>
                        <div class="mt-3 sm:mt-5">
                            <h4 class="font-bold tracking-wide border-b border-hoverLight pb-3" v-if="(isLoaded && !admin) || (isLoaded && admin && userView)">{{helpTitle}}</h4>
                            <vue-input for="helpTitle" id="helpTitle" v-model="helpTitle" v-if="editPermissions && !this.userView">Title</vue-input>
                            <div class="mt-2 space-y-4">
                                <VueLoading v-if="!isLoaded"></VueLoading>
                                <vue-editor v-model="helpContent" v-if="isLoaded && editPermissions && !userView"></vue-editor>
                                <p class="tracking-wide border-t border-b border-hoverLight p-3" v-if="editPermissions && !userView">Preview</p>
                                <div v-html="helpContent"></div>
                            </div>
                        </div>
                    </div>
                    <div class="flex flex-1 justify-center space-x-2 mt-5">
                        <vue-button type="button" @click="saveContent" v-if="editPermissions">Submit changes</vue-button>
                        <vue-button varient="danger" type="button" @click="close">Close</vue-button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import { VueEditor } from "vue2-editor";
    import VueLoading from '../components/VueLoading';
    import fieldButton from '@/components/CustomFields/fieldButton';
    import fieldInput from '@/components/CustomFields/fieldInput';
    import PageMixin from '@/mixins/page-mixin';

    export default {
        name: "HelpDocumentation",

        components: {
            VueEditor,
            VueLoading,
            'vue-button': fieldButton,
            'vue-input': fieldInput
        },

        mixins: [PageMixin],

        props: {
            HelpContentKey: {
                type: String,
                required: true
            }
        },

        data() {
            return {
                isLoaded: false,
                userView: true,
                helpTitle: '',
                helpContent: '',
                isActive: true
            }
        },

        beforeMount() {
            this.pageMounting();
        },

        mounted() {
            this.pageMounted().then(() => {
                this.getData();
                this.pageReady();
            })
        },

        computed: {
            editPermissions() {
                return (this.admin || this.masterAdmin)
            }
        },

        beforeDestroy() {
        },

        methods: {
            getData() {
                var key = this.HelpContentKey;
                var admin = this.admin;
                var docInfo = { "HelpContentKey": key, "IsAdmin": admin }
                this.$store.dispatch('getDocumentation', docInfo).then(() => {
                    this.helpContent = this.$store.getters.helpContent;
                    this.helpTitle = this.$store.getters.helpTitle;
                    this.isActive = this.$store.getters.helpIsActive;
                    this.isLoaded = true;
                }).catch((err) => {
                    console.log(err)
                    this.error("Error getting documentation")
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
                var admin = this.admin;

                this.$store.dispatch('updateDocumentation', { helpContentKey, helpTitle, helpContent, isActive, userId, admin }).then(() => {
                    this.helpContent = this.$store.getters.helpContent;
                    this.helpTitle = this.$store.getters.helpTitle;
                    this.isActive = this.$store.getters.helpIsActive;
                    this.isLoaded = true;
                    this.success("Content updated")
                }).catch((err) => {
                    this.error("Error updating content");
                })
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

<!--<style>
    ol, ul {
        list-style: disc !important;
        padding-top: 16px !important;
        padding-left: 40px !important;
    }
</style>-->