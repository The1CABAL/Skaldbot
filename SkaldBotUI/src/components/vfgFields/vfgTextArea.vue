<template>
    <vue-text-area :placeholder="schema.placeholder" :required="schema.required" :is-disabled="schema.disabled" v-model="value" :rows="schema.rows">{{schema.fieldLabel}}</vue-text-area>
</template>

<script>
    import { abstractField } from "vue-form-generator";
    import fieldTextArea from '@/components/CustomFields/fieldTextArea'

    export default {
        name: "vfgInput",

        mixins: [abstractField],

        components: {
            'vue-text-area': fieldTextArea
        }
    }
</script>