<template>
    <div class="form">
        <div v-if="!loaded">
            <VueLoading></VueLoading>
        </div>

        <div v-if="submitted" v-bind:class="isError ? 'errorMsg' : 'successMsg'">
            <p style="font-weight: bold;">{{msg}}</p>
            <button class="close" @click="closeNotification">x</button>
        </div>

        <div v-if="loaded" class="panel">
            <div class="panel-heading">{{formName}}</div>
            <hr />
            <div class="panel-body">
                <form action="" v-on:submit="formSubmit">
                    <vue-form-generator v-if="loaded" :schema="schema" :model="model" :options="formOptions" v-on:validated="validateForm"></vue-form-generator>
                </form>
            </div>
        </div>
        <div v-if="admin">
            <input type="checkbox" id="cbShowFormDetails" name="cbShowFormDetails" v-on:change="showFormDetails" />
            <label for="cbShowFormDetails">Show Form Information</label>
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
</template>

<script>
    import axios from 'axios'
    import VueLoading from '../VueLoading';
    import VueFormGenerator from 'vue-form-generator'
    import "vue-form-generator/dist/vfg.css";  // optional full css additions
    import { mapGetters, mapActions } from "vuex";
    import { BaseUrl } from '../../helpers/constants';

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
        },
        props: {
            formKey: {
                type: String,
                required: true
            }
        },
        mounted: function () {
            this.loaded = false;
            let schemaUrl = BaseUrl + "getFormSchema?formKey=" + this.formKey;
            let actionUrl = BaseUrl + "getActionLink?formKey=" + this.formKey;
            let nameUrl = BaseUrl + "getFormName?formKey=" + this.formKey;
            var that = this;
            axios.get(schemaUrl).then(function (response) {
                that.schema = JSON.parse(response.data);
            }).catch(function (error) {
                console.log(error);
                this.$emit('error', true)
            });

            axios.get(actionUrl).then(function (response) {
                //console.log(JSON.parse(response.data));
                var data = JSON.parse(response.data);
                var actionLink = data[0];
                //console.log(actionLink.ActionLink);
                that.action = baseUrl + actionLink.ActionLink;
                //console.log(that.action);
            }).catch(error => { console.log(error) });

            axios.get(nameUrl).then(function (response) {
                var data = JSON.parse(response.data);
                var name = data[0].FormName;
                that.formName = name;
                that.loaded = true;
            }).catch(error => { console.log(error) });
        },
        watch: {
            formKey: function () {
                this.loaded = false;
                let baseUrl = "http://127.0.0.1:5000"
                let schemaUrl = BaseUrl + "getFormSchema?formKey=" + this.formKey;
                let actionUrl = baseUrl + "getActionLink?formKey=" + this.formKey;
                let nameUrl = BaseUrl + "getFormName?formKey=" + this.formKey;
                var that = this;
                axios.get(schemaUrl).then(function (response) {
                    that.schema = JSON.parse(response.data);
                }).catch(function (error) {
                    console.log(error);
                    this.$emit('error', true)
                });

                axios.get(actionUrl).then(function (response) {
                    //console.log(JSON.parse(response.data));
                    var data = JSON.parse(response.data);
                    var actionLink = data[0];
                    //console.log(actionLink.ActionLink);
                    that.action = baseUrl + actionLink.ActionLink;
                }).catch(error => { console.log(error) });

                axios.get(nameUrl).then(function (response) {
                    var data = JSON.parse(response.data);
                    var name = data[0].FormName;
                    that.formName = name;
                    that.loaded = true;
                }).catch(error => { console.log(error) });
            },
            loaded: function () {
                if (this.loaded) {
                    this.newModel();
                }
            },
            submitted: function () {
                if (this.submitted) {
                    setTimeout(
                        this.closeNotification, 5000);
                }
            }
        },
        data() {
            return {
                action: '',
                model: {},
                schema: null,
                options: {
                    validatedAfterLoad: false,
                    validatedAfterChange: true
                },
                loaded: false,
                msg: '',
                isError: false,
                submitted: false,
                admin: false,
                formName: 'Test',
                showFormExtras: false,
                isValid: false,
                formOptions: {
                    validateAfterLoad: false,
                    validateAfterChanged: true
                },
            }
        },
        created() {
            console.log(this.$store.getters.isAdmin);
            console.log(this.$store.getters.isMasterAdmin);
            if (this.$store.getters.isAdmin || this.$store.getters.isMasterAdmin) {
                this.admin = true
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
                    //console.log(url);
                    if (this.formKey == "LoginForm" || this.formKey == "RegisterForm") {
                        var username = this.model.username;
                        var password = this.model.password;
                        //console.log(this.formKey);
                        if (this.formKey == "LoginForm")
                            this.$store.dispatch('login', { username, password }).then(() => this.$emit("LoginSuccess", true)).catch(err => console.log(err))
                        else {
                            var firstname = this.model.firstname;
                            var lastname = this.model.lastname;
                            this.$store.dispatch('register', { username, firstname, lastname, password }).then(() => this.$emit("RegisterSuccess", true)).catch(err => console.log(err))
                        }
                    }
                    else {
                        axios.post(url, this.model).then(function (response) {
                            var returnVal = response.data;
                            if (returnVal.Message.toString() == "Success") {
                                that.setNotification(true);
                            }
                            else {
                                //console.log("Setting success to false");
                                that.setNotification(false);
                            }
                        });
                    }
                }
                event.preventDefault();

            },
            setNotification(success) {
                if (success) {
                    this.submitted = true;
                    this.msg = "Successfully submitted the suggestion!";
                }
                else {
                    this.submitted = true;
                    this.isError = true;
                    this.msg = "There was an error submitting the suggestion. Please try again.";
                }
            },
            closeNotification() {
                this.msg = '';
                this.submitted = false;
            },
            showFormDetails() {
                if (this.showFormExtras)
                    this.showFormExtras = false;
                else
                    this.showFormExtras = true;
            }
        },
        computed: {
            ...mapGetters(["formSchema", "isAdmin", "isMasterAdmin", "isUser"])
        }
    }
</script>

<style scoped>
    .close {
        position: absolute;
        font-size: 15px;
        top: 1px;
        right: 0;
        border: 0;
        padding-right: 5px;
        background-color: rgba(0,0,0,0.0);
    }

    .successMsg {
        position: relative;
        display: inline-block;
        width: 100%;
        height: auto;
        background: #93FFA1;
        border-radius: 10px 10px 10px 10px;
        overflow: hidden;
        padding-left: 10px;
    }

    .errorMsg {
        position: relative;
        display: inline-block;
        width: 100%;
        height: auto;
        background: #FF9393;
        border-radius: 10px 10px 10px 10px;
        overflow: hidden;
        padding-left: 10px;
    }

    .form {
        padding-top: 15px;
    }

    .panel {
        margin-bottom: 20px;
        background-color: #fff;
        border: 1px solid transparent;
        border-radius: 4px;
        -webkit-box-shadow: 0 1px 1px rgba(0, 0, 0, .05);
        box-shadow: 0 1px 1px rgba(0, 0, 0, .05);
        border-color: #ddd;
    }

    .panel-heading {
        color: #333;
        background-color: #f5f5f5;
        border-color: #ddd;
        padding: 10px 15px;
        border-bottom: 1px solid transparent;
        border-top-left-radius: 3px;
        border-top-right-radius: 3px;
    }

    .panel-body {
        padding: 15px;
    }
</style>