<template>
    <div id="filtered-table">
        <div class="flex-1 flex justify-between pb-3">
            <vue-select
                        v-if="showPerPage"
                        :items="itemsPerPage"
                        @change="perPageChange"
                        :show-select-option="false"
                        :default-selected-item="defaultPerPageOption" />

            <vue-search-input class="justify-end" v-model="searchValue" v-if="showSearchField" />
        </div>
        <vue-table :items="items"
                   :action-button-options="actionButtonOptions"
                   :hidden-columns="hiddenColumns"
                   @editClick="editClick">
            <slot></slot>
        </vue-table>
        <nav class="border-t border-gray-200 px-4 flex items-center justify-between sm:px-0 bg-white rounded-md pb-3 mt-3" v-if="showPagination">
            <div class="-mt-px w-0 flex-1 flex">
                <a href="#" class="border-t-2 border-transparent pt-3 pl-2 pr-1 inline-flex items-center text-sm font-medium text-gray-500 hover:text-gray-700 hover:border-gray-300">
                    <!-- Heroicon name: solid/arrow-narrow-left -->
                    <svg class="mr-3 h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                        <path fill-rule="evenodd" d="M7.707 14.707a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l2.293 2.293a1 1 0 010 1.414z" clip-rule="evenodd" />
                    </svg>
                    Previous
                </a>
            </div>
            <div class="hidden md:-mt-px md:flex">
                <a v-for="page in pages" 
                   :key="page" 
                   href="#" 
                   class="border-t-2 pt-4 px-4 inline-flex items-center text-sm font-medium" 
                   :class="{'border-indigo-500 text-indigo-600' : isPageSelected(page), 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300' : !isPageSelected(page)}"
                   aria-current="isPageSelected(page)">
                    {{page}}
                </a>
            </div>
            <div class="-mt-px w-0 flex-1 flex justify-end">
                <a href="#" class="border-t-2 border-transparent pt-3 pr-2 pl-1 inline-flex items-center text-sm font-medium text-gray-500 hover:text-gray-700 hover:border-gray-300">
                    Next
                    <!-- Heroicon name: solid/arrow-narrow-right -->
                    <svg class="ml-3 h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                        <path fill-rule="evenodd" d="M12.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-2.293-2.293a1 1 0 010-1.414z" clip-rule="evenodd" />
                    </svg>
                </a>
            </div>
        </nav>
    </div>
</template>

<script>
    import fieldSelect from '@/components/CustomFields/fieldSelect';
    import fieldSearchInput from '@/components/CustomFields/fieldSearchInput';
    import UtilMixin from '@/mixins/util-mixin';
    import vueTable from '@/components/Tables/vueTable'

    export default {
        name: "FilteredTable",

        mixins: [UtilMixin],

        props: {
            showPerPage: {
                type: Boolean,
                default: false
            },

            defaultPerPageOption: {
                type: Number,
                default: 10
            },

            showSearchField: {
                type: Boolean,
                default: false
            },

            showPagination: {
                type: Boolean,
                default: false
            },

            items: {
                type: Array,
                default: () => []
            },

            pages: {
                type: Number,
                default: 1
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

        components: {
            'vue-select': fieldSelect,
            'vue-search-input': fieldSearchInput,
            'vue-table': vueTable
        },

        data() {
            return {
                itemsPerPage: [
                    {
                        name: '10',
                        value: 10
                    },
                    {
                        name: '20',
                        value: 20
                    },
                    {
                        name: '50',
                        value: 50
                    },
                    {
                        name: '100',
                        value: 100
                    },
                ],
                perPage: null,
                searchValue: '',
                selectedPage: 1
            }
        },

        methods: {
            perPageChange(page) {
                if (!this.showPerPage) {
                    return;
                };

                this.perPage = page.value;

                this.emit('perPageChange', this.perPage)
            },

            searchFieldChange() {
                this.emit('search', this.searchValue);
            },

            isPageSelected(page) {
                return this.selectedPage === page;
            },

            editClick(e) {
                this.$emit('editClick', e)
            }
        },

        watch: {
            searchValue(newVal, oldVal) {
                if (newVal !== oldVal) {
                    this.debounce(this.searchFieldChange, 2000);
                }
            }
        }
    }
</script>