<template>
    <div class="flex flex-col">
        <div class="overflow-x-auto justify-center w-full">
            <div class="py-2 align-middle inline-block min-w-full">
                <div class="shadow overflow-hidden border-b border-gray-200 sm:rounded-lg">
                    <table class="min-w-full divide-y divide-gray-200">
                        <thead class="bg-primaryLight">
                            <tr>
                                <slot>

                                </slot>
                                <vue-table-column v-if="actionButtonOptions.Visible" label="Action" prop="Action" />
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(item, itemsIdx) in items" :key="itemsIdx" :class="itemsIdx % 2 === 0 ? 'bg-primary' : 'bg-primaryLight'" v-if="hasItems">
                                <td v-for="(key, index) in item"
                                    v-if="!isItemHidden(index)"
                                    :key="'row-' + itemsIdx + '-item-'+index"
                                    class="px-6 py-4 whitespace-nowrap text-sm truncate max-w-md"
                                    :class="{'font-medium text-gray-900' : index === 0}">
                                    {{cleanseValue(key)}}
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium" v-if="actionButtonOptions.Visible">
                                    <a href="#" @click.prevent="editClick(item)" class="text-hover hover:text-hoverLight">{{actionButtonOptions.Label}}</a>
                                </td>
                            </tr>
                            <tr class="bg-primary" v-if="!hasItems">
                                <td :colspan="totalCols" class="px-6 py-4 whitespace-nowrap">
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
            if (this.actionButtonOptions.Visible) {
                this.totalCols = this.$slots.default.length + 1;
                return;
            }
            this.totalCols = this.$slots.default.length;
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
                    return this.getTrueString(value);
                }

                let letterRegex = /^(\d{4}-\d{2}-\d{2}[tT]\d{2}:\d{2}:\d{2}.*)$/;

                if (typeof methodValue === 'string' && new Date(methodValue) != 'Invalid Date' && methodValue.match(letterRegex)) {
                    return this.getDate(methodValue);
                }

                return methodValue;
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