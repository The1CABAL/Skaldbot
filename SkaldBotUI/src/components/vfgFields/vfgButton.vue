<template>
    <vue-button :type="schema.buttonType" :id="schema.id" :varient="schema.varient">{{schema.buttonText}}</vue-button>
</template>

<script>
    import { abstractField } from "vue-form-generator";
    import fieldButton from '@/components/CustomFields/fieldButton'

    export default {
        name: "vfgButton",

        mixins: [abstractField],

        components: {
            'vue-button': fieldButton
        }
    }
</script>