<template>
    <div>
        <input class="form-control"
               :type="passwordFieldType"
               v-model="value"
               :disabled="schema.disabled"
               :maxlength="schema.max"
               :placeholder="schema.placeholder"
               :readonly="schema.readonly"
               :validators="schema.validators"
               :showButton="schema.showButton">
        <input type="checkbox" id="togglePassword" v-if="showButton" v-on:click="showPassword" />
        <label for="togglePassword" v-if="showButton">Show Password</label>
    </div>
</template>

<script>
    import { abstractField } from "vue-form-generator";

    export default {
        name: "passwordField",
        mixins: [abstractField],
        data() {
            return {
                showButton: false,
                passwordFieldType: 'password'
            }
        },
        mounted() {
            this.showButton = this.schema.showButton;
        },
        watch: {
            showButton: function (newValue, oldValue) {
                if (newValue != oldValue) {
                    this.showButton = newValue;
                }
            }
        },
        methods: {
            showPassword() {
                if (this.passwordFieldType == "password") {
                    this.passwordFieldType = "text"
                }
                else {
                    this.passwordFieldType = "password";
                }
            }
        }
    }
</script>

<style scoped>
    div{
        width: 100%
    }
    .form-control{
        width: 100%;
    }
</style>