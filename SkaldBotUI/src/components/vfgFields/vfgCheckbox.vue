<template>
    <vue-checkbox :id="schema.id" v-model="value">{{schema.fieldLabel}}</vue-checkbox>
</template>

<script>
    import { abstractField } from "vue-form-generator";
    import fieldCheckbox from '@/components/CustomFields/fieldCheckbox'

    export default {
        name: "vfgButton",

        mixins: [abstractField],

        components: {
            'vue-checkbox': fieldCheckbox
        }
    }
</script>