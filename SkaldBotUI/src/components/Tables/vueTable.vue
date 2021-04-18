<template>
    <div class="flex flex-col">
        <div class="-my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
            <div class="py-2 align-middle inline-block min-w-full sm:px-6 lg:px-8">
                <div class="shadow overflow-hidden border-b border-gray-200 sm:rounded-lg">
                    <table class="min-w-full divide-y divide-gray-200">
                        <thead class="bg-gray-50">
                            <tr>
                                <slot>

                                </slot>
                                <vue-table-column v-if="actionButtonOptions.Visible" label="Action"/>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(item, itemsIdx) in items" :key="itemsIdx" :class="itemsIdx % 2 === 0 ? 'bg-white' : 'bg-gray-100'" v-if="hasItems">
                                <td v-for="(key, index) in item" 
                                    v-if="!isItemHidden(index)"
                                    :key="'row-' + itemsIdx + '-item-'+index" 
                                    class="text-primary px-6 py-4 whitespace-nowrap text-sm" 
                                    :class="{'font-medium text-gray-900' : index === 0}">
                                    {{cleanseValue(key)}}
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium" v-if="actionButtonOptions.Visible">
                                    <a href="#" @click.prevent="editClick(item)" class="text-indigo-600 hover:text-indigo-900">{{actionButtonOptions.Label}}</a>
                                </td>
                            </tr>
                            <tr class="bg-white" v-if="!hasItems">
                                <td :colspan="totalCols" class="text-primary px-6 py-4 whitespace-nowrap">
                                    <p class="text-center font-bold text-md">No data</p>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import UtilMixin from '@/mixins/util-mixin'
    import vueTableColumn from '@/components/Tables/vueTableColumn'

    export default {
        name: "VueTable",

        mixins: [UtilMixin],

        components: {
            'vue-table-column': vueTableColumn
        },

        props: {
            items: {
                type: Array,
                required: true
            },

            actionButtonOptions: {
                type: Object,
                default: () => {
                    return {
                        Visible: true,
                        Label: 'Edit',
                        EmitValue: 'Id'
                    }
                }
            },

            hiddenColumns: {
                type: Array,
                default: () => []
            }
        },

        data() {
            return {
                 totalCols: 1
            }
        },

        mounted() {
            this.totalCols = this.$slots.default.length
        },

        methods: {
            isItemHidden(column) {
                return this.hiddenColumns.includes(column);
            },

            cleanseValue(value) {
                let methodValue = ''

                if (typeof value === 'string') {
                    methodValue = value.toLowerCase();
                }
                else {
                    methodValue = value;
                }

                if (methodValue === 'true' || methodValue === 'false' || typeof methodValue === 'boolean') {
                    return this.getTrueString(value == 'true');
                }

                if (Date.parse(methodValue)) {
                    return this.getDate(methodValue);
                }

                if (typeof methodValue === 'string') {
                    return methodValue;
                }
            },

            editClick(item) {
                if (typeof item !== 'object') {
                    return;
                }

                this.$emit('editClick', item[this.actionButtonOptions.EmitValue])
            }
        },

        computed: {
            hasItems() {
                return this.items.length > 0;
            }
        }
    }
</script>