<template>
    <div class="form">
        <div v-if="!loaded">
            <VueLoading></VueLoading>
        </div>

        <div v-if="loaded">
            <div class="panel">
                <div v-if="showFormName">
                    <div class="flex flex-1 justify-between">
                        <h2 class="font-bold tracking-wide ml-3 mt-3">{{formName}}</h2>
                        <vue-button varient="close" @click="close" aria-label="Close modal" v-if="showCloseButton">x</vue-button>
                    </div>
                    <hr class="my-3" />
                </div>
                <div class="panel-body">
                    <form action="" v-on:submit.prevent="formSubmit">
                        <vue-form-generator v-if="loaded" :schema="schema" :model="model" :options="formOptions" v-on:validated="validateForm"></vue-form-generator>
                    </form>
                </div>
            </div>
            <div v-if="admin">
                <vue-checkbox @change="showFormDetails">Show Form Information</vue-checkbox>
            </div>
            <div v-if="showFormExtras" class="panel panel-default">
                <div class="panel-heading">Model</div>
                <div class="panel-body">
                    <pre v-if="model" v-html="prettyJSON(model)"></pre>
                </div>
            </div>

            <div v-if="showFormExtras" class="panel panel-default">
                <div class="panel-heading">Schema</div>
                <div class="panel-body">
                    <pre v-if="model" v-html="prettyJSON(schema)"></pre>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import VueLoading from '../VueLoading';
    import VueFormGenerator from 'vue-form-generator'
    import "vue-form-generator/dist/vfg.css";  // optional full css additions
    import { mapActions } from "vuex";
    import fieldCheckbox from "../CustomFields/fieldCheckbox.vue";
    import fieldButton from '../CustomFields/fieldButton';
    import PageMixin from '@/mixins/page-mixin'

    VueFormGenerator.validators.emailValidation = function (value, field, model) {
        let email = model.email;
        let confEmail = value;

        if (email != confEmail) {
            return ["Emails do not match!"];
        } else {
            return [];
        }
    }

    VueFormGenerator.validators.passwordValidation = function (value, field, model) {
        let password = model.password;
        let confPassword = value;

        if (password != confPassword) {
            return ["Passwords do not match!"];
        }
        else {
            return [];
        }
    }

    export default {
        name: "Form",

        components: {
            VueLoading,
            'vue-checkbox': fieldCheckbox,
            'vue-button': fieldButton
        },

        mixins: [PageMixin],

        props: {
            formKey: {
                type: String,
                required: true
            },
            accountId: {
                type: String,
                required: false
            },
            passedModel: {
                type: [Object, Array],
                required: false
            },
            showCloseButton: {
                type: Boolean,
                default: false
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

        watch: {
            formKey() {
                this.getData();
            },

            loaded() {
                if (this.loaded) {
                    this.newModel();
                }
            },

            submitted() {
                if (this.submitted) {
                    setTimeout(
                        this.closeNotification, 5000);
                }
            },

            passedModel() {
                if (this.passedModel != undefined && this.passedModel != null)
                    this.setModel();
            }
        },

        data() {
            return {
                action: '',
                model: {},
                schema: null,
                showFormName: true,
                options: {
                    validatedAfterLoad: false,
                    validatedAfterChange: true
                },
                loaded: false,
                msg: '',
                isError: false,
                submitted: false,
                formName: 'Test',
                showFormExtras: false,
                isValid: false,
                formOptions: {
                    validateAfterLoad: false,
                    validateAfterChanged: true
                },
            }
        },

        methods: {
            ...mapActions(["fetchFormData"]),

            prettyJSON: function (json) {
                if (json) {
                    json = JSON.stringify(json, undefined, 4);
                    json = json.replace(/&/g, '&').replace(/</g, '<').replace(/>/g, '>');
                    return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, function (match) {
                        var cls = 'number';
                        if (/^"/.test(match)) {
                            if (/:$/.test(match)) {
                                cls = 'key';
                            } else {
                                cls = 'string';
                            }
                        } else if (/true|false/.test(match)) {
                            cls = 'boolean';
                        } else if (/null/.test(match)) {
                            cls = 'null';
                        }
                        return '<span class="' + cls + '">' + match + '</span>';
                    });
                }
            },

            newModel() {
                if (this.formKey != "LoginForm")
                    this.model = VueFormGenerator.schema.createDefaultObject(this.schema);
            },

            validateForm(isValid) {
                this.isValid = isValid;
            },

            formSubmit() {
                if (this.isValid) {
                    var url = this.action;
                    let that = this;
                    if (this.formKey == "LoginForm" || this.formKey == "RegisterForm" || this.formKey == "RegisterUserForm") {
                        if (this.formKey == "LoginForm") {
                            this.dispatchLogin();
                        }
                        else if (this.formKey == "RegisterForm") {
                            this.dispatchRegisterAccount();
                        }
                        else if (this.formKey == "RegisterUserForm") {
                            this.dispatchRegisterUser();
                        }
                    }
                    else {
                        this.dispatchForm();
                    }
                }
                else {
                    this.setNotification(false);
                }
            },

            dispatchLogin() {
                let { username, password } = this.model;
                this.$store.dispatch('login', { username, password })
                    .then(resp => resp.statusText == "OK" ? this.$emit("LoginSuccess", true) : this.error("Error"))
                    .catch(err => { this.error("There was an error signing in. Please confirm your user name and password are correct.") })
            },

            dispatchRegisterAccount() {
                var firstname = this.model.firstname;
                var lastname = this.model.lastname;
                var accountname = this.model.accountName;
                var discorduserid = this.model.discordUserId;

                this.$store.dispatch('register', { accountname, username, firstname, lastname, discorduserid, password })
                    .then(() => { this.dispatchLogin(); })
                    .catch(err => this.error('There was an error registering. Please try agian later.'))
            },

            dispatchRegisterUser() {
                var firstname = this.model.firstname;
                var lastname = this.model.lastname;
                var accountid = this.accountId;
                var discorduserid = this.model.discordUserId;
                this.$store.dispatch('registeruser', { accountid, username, firstname, lastname, discorduserid, password })
                    .then(() => this.success('User created!'))
                    .catch(err => this.error('There was an error registering. Please try agian later.'))
            },

            dispatchForm() {
                let model = this.model;
                let that = this;

                this.$store.dispatch('postFormData', { url, model }).then(() => {
                    var returnVal = this.$store.getters.getPostStatus;
                    if (returnVal == "Success") {
                        that.setNotification(true);
                    }
                    else {
                        that.setNotification(false);
                    }
                }).catch(err => {
                    console.log(err);
                    this.error("Error submitting form");
                })
            },

            setNotification(success) {
                if (success) {
                    this.submitted = true;
                    this.success("Successfully submitted!");

                    if (this.formKey == "ManageServer")
                        this.$emit("ServerSuccess", true);
                    else if (this.formKey == "UpdatePassword")
                        this.$emit("PasswordSuccess", true);
                }
                else {
                    this.submitted = true;
                    this.isError = true;
                    this.error("There was an error submitting. Please try again.");
                }
            },

            showFormDetails() {
                if (this.showFormExtras)
                    this.showFormExtras = false;
                else
                    this.showFormExtras = true;
            },

            getData() {
                this.$store.dispatch('fetchForm', this.formKey).then(() => {
                    this.schema = JSON.parse(this.$store.getters.getFormSchema);
                    this.action = this.$store.getters.getFormActionLink;
                    this.formName = this.$store.getters.getFormName;
                    this.showFormName = this.$store.getters.getShowFormName;

                    if (this.passedModel != undefined && this.passedModel != null) {
                        this.setModel();
                    }
                    else {
                        this.newModel();
                    }

                    this.loaded = true;
                }).catch((err) => {
                    console.log(err);
                    this.error('Error getting form data');
                })
            },

            setModel() {
                if (this.passedModel[0] != undefined && this.passedModel[0] != null) {
                    this.model = VueFormGenerator.schema.createDefaultObject(this.schema, this.passedModel[0])
                }
            },

            close() {
                this.$emit('close');
            }
        }
    }
</script>