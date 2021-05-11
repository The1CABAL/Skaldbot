<template>
    <div>
        <vue-input
               :type="passwordFieldType"
               v-model="value"
               :disabled="schema.disabled"
               :maxlength="schema.max"
               :placeholder="schema.placeholder"
               :readonly="schema.readonly">
            {{schema.fieldLabel}}
            </vue-input>
        <vue-checkbox id="togglePassword" v-if="showButton" v-on:change="showPassword">Show Password</vue-checkbox>
    </div>
</template>

<script>
    import { abstractField } from "vue-form-generator";
    import fieldInput from '@/components/CustomFields/fieldInput'
    import fieldCheckbox from '@/components/CustomFields/fieldCheckbox'

    export default {
        name: "passwordField",
        mixins: [abstractField],

        data() {
            return {
                showButton: false,
                passwordFieldType: 'password'
            }
        },

        components: {
            'vue-input': fieldInput,
            'vue-checkbox': fieldCheckbox
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