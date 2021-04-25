<template>
    <vue-input :placeholder="schema.placeholder" :required="schema.required" :is-disabled="schema.disabled" v-model="value">{{schema.fieldLabel}}</vue-input>
</template>

<script>
    import { abstractField } from "vue-form-generator";
    import fieldInput from '@/components/CustomFields/fieldInput'

    export default {
        name: "vfgInput",

        mixins: [abstractField],

        components: {
            'vue-input': fieldInput
        }
    }
</script>