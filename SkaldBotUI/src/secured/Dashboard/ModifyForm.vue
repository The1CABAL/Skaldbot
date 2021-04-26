<template>
    <div id="ModifyForm" class="h-full overflow-x-auto">
        <vue-button type="button" v-on:click="goBack">Go Back</vue-button>
        <div v-show="modalVisible">
            <transition name="modal-fade">
                <div class="fixed z-10 inset-0 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
                    <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
                        <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" aria-hidden="true"></div>
                        <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
                        <div class="inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-sm sm:w-full sm:p-6">
                            <div>
                                <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-yellow-100">
                                    <svg class="h-6 w-6 text-yellow-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                                    </svg>
                                </div>
                                <div class="mt-3 text-center sm:mt-5">
                                    <h3 class="text-lg leading-6 font-medium text-gray-900" id="modal-title">
                                        Submit?
                                    </h3>
                                    <div class="mt-2">
                                        <p class="text-sm text-gray-500">
                                           Are you sure you want to submit?
                                        </p>
                                    </div>
                                </div>
                            </div>
                            <div class="flex flex-1 justify-center space-x-2 mt-2">
                                <vue-button type="button" @click="formSubmit">Yes, submit</vue-button>
                                <vue-button varient="danger" type="button" @click="close">No, cancel</vue-button>
                            </div>
                        </div>
                    </div>
                </div>
            </transition>
        </div>
        <div class="panel" v-if="loaded">
            <div class="panel-body">
                <h4 class="font-semibold">{{formName}} Form</h4>
                <hr class="mt-3 mb-3" />
                <form v-on:submit="showModal">
                    <vue-input id="formName" name="formName" v-model="formName" required>Form Name</vue-input>
                    <vue-input id="formKey" name="formKey" v-model="formData.FieldInfo.FormKey" required>Form Key</vue-input>
                    <vue-input id="actionLink" name="actionLink" v-model="formData.FieldInfo.ActionLink" required>Action Link</vue-input>
                    <vue-checkbox id="isActive" name="isActive" v-model="formData.FieldInfo.IsActive">Is Active</vue-checkbox>
                    <vue-text-area id="formSchema" name="formSchema" v-model="formData.FieldInfo.FieldSchema" rows="10">Field Schema</vue-text-area>
                    <div class="w-full space-x-2">
                        <vue-button type="submit">Submit</vue-button>
                        <!--<vue-button varient="secondary" @click="updateFieldSchema">Refresh Form</vue-button>-->
                    </div>
                </form>
                <section v-if="hasSchema" class="pt-3">
                    <hr class="pt-3" />
                    <h4 class="font-semibold tracking-wide pb-3">Form View</h4>
                    <hr class="pb-3" />
                    <vue-form-generator v-if="loaded" :schema="schema" :model="model" :options="formOptions"></vue-form-generator>
                </section>
            </div>
        </div>
    </div>
</template>

<script>
    import PageMixin from '@/mixins/page-mixin'
    import UtilMixin from '@/mixins/util-mixin'
    import fieldInput from '@/components/CustomFields/fieldInput'
    import fieldCheckbox from '@/components/CustomFields/fieldCheckbox'
    import fieldTextArea from '@/components/CustomFields/fieldTextArea'
    import fieldButton from '@/components/CustomFields/fieldButton'
    import Vue from 'vue';

    export default {
        name: "ModifyForm",

        props: {
            formKey: {
                type: String,
                required: false
            }
        },

        mixins: [PageMixin, UtilMixin],

        components: {
            'vue-input': fieldInput,
            'vue-checkbox': fieldCheckbox,
            'vue-text-area': fieldTextArea,
            'vue-button': fieldButton
        },

        data() {
            return {
                loaded: false,
                formName: '',
                isNewForm: false,
                modalVisible: false,
                formData: [],
                schema: [],
                model: {},
                formOptions: {
                    validateAfterLoad: false,
                    validateAfterChanged: true
                },
            }
        },

        beforeMount() {
            this.pageMounting();
        },

        computed: {
            hasSchema() {
                return this.formData.FieldInfo.FieldSchema.length > 0;
            }
        },

        mounted() {
            this.pageMounted().then(() => {
                if (!this.masterAdmin && !this.admin) {
                    this.redirectUser('/unauthorized');
                    return;
                }

                this.fetchData();
                this.pageReady();
            })
        },

        methods: {
            fetchData() {
                if (this.formKey == null || this.formKey == '') {
                    this.setNewForm();
                    this.loaded = true;
                    return; 
                }

                this.loaded = false;
                return this.$store.dispatch('fetchForm', this.formKey).then(() => {
                    this.getData();
                });
            },

            setNewForm() {
                const defaultSchema = {
                    FormKey: '',
                    ActionLinke: '',
                    IsActive: false,
                    FieldSchema: ''
                };

                Vue.set(this.formData, 'FieldInfo', defaultSchema);
            },

            getData() {
                this.formData = this.$store.getters.getForm
                this.schema = JSON.parse(this.formData.FieldInfo.FieldSchema)
                this.formName = this.formData.FormInfo.FormName;
                this.loaded = true;
            },

            formSubmit() {
                this.modalVisible = false;

                var data = this.formData;
                var userId = this.$store.getters.userId;
                var isNew = this.isNewForm;
                var formName = this.formName;

                if (this.isNewForm) {
                    var formKey = this.formData.FieldInfo.FormKey
                    var actionLink = this.formData.FieldInfo.ActionLink

                    data = { "FormKey": formKey, "FieldSchema": this.formData.FieldInfo.FieldSchema, "ActionLink": actionLink, "IsActive": false }
                }

                this.$store.dispatch('updateForm', { data, userId, isNew, formName })
                    .then(resp => { resp.statusText == "OK" ? this.success("Form was updated!") : this.error("There was an error updating the form"); this.fetchData(); })
                    .catch(err => console.log(err));

                event.preventDefault();
            },

            showModal() {
                this.modalVisible = true;
                event.preventDefault();
            },

            close() {
                this.modalVisible = false;
            },

            goBack() {
                this.$router.push('/manageforms')
            },
        },

        watch: {
            'formData.FieldInfo.FieldSchema'(newVal, oldVal) {
                if (!this.areEquivalent(newVal, oldVal)) {
                    let updateSchema = function () {
                        this.schema = JSON.parse(newVal)
                    }
                    this.debounce(updateSchema, 2000);
                }
            }
        }
    }
</script>