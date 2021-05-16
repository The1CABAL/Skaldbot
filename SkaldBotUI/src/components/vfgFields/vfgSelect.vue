<template>
    <vue-select 
                :label="schema.fieldLabel" 
                :show-select-option="displaySelectKeywordItem"
                :items="localItems"
                :v-if="hasItems"
                @change="setValue"/>
</template>

<script>
    import fieldSelect from '@/components/CustomFields/fieldSelect.vue';
    import { abstractField } from "vue-form-generator";
    import vfgMixin from '@/mixins/vfg-mixin.js'
    import axios from 'axios'
    import { BaseUrl } from '../../helpers/constants';

    export default {
        name: "vfgSelect",

        components: {
            'vue-select': fieldSelect
        },

        mixins: [abstractField, vfgMixin],

        data() {
            return {
                localItems: [],
            }
        },

        methods: {
            getItems() {
                if (this.dataSourceId <= 0) {
                    console.error("vfgSelect was initialized with empty datasource id");
                    return;
                }

                axios.get(`${BaseUrl}selectItems`, {
                    params: {
                        id: this.dataSource
                    }
                }).then((resp) => {
                    this.localItems = JSON.parse(resp.data.Items)
                })
            },

            setValue(val) {
                this.value = val.value;
            }
        },

        computed: {
            displaySelectKeywordItem() {
                return this.schema.showSelectOption === undefined ? true : this.schema.showSelectOption;
            },

            hasItems() {
                return this.localItems.length > 0;
            },

            dataSource() {
                return this.schema.dataSourceId ? this.schema.dataSourceId : 0;
            }
        }
    }
</script>