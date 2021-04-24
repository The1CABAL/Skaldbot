<template>
    <div id="filtered-table">
        <div class="flex-1 flex justify-between pb-3">
            <vue-select class="w-1/4"
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
            <vue-table-column v-for="column in columns" :prop="column.prop" :label="column.label" :key="column.prop" :is-sortable="column.sortable" @sort="setSort"/>
        </vue-table>
        <nav class="px-4 flex items-center justify-between sm:px-0 bg-primaryLight rounded-md pb-3 mt-3" v-if="showPagination">
            <div class="-mt-px w-0 flex-1 flex">
                <a href="#" class="border-t-2 border-transparent pt-3 pl-2 pr-1 inline-flex items-center text-sm font-medium hover:text-hover hover:border-gray-300" v-if="hasPrevious" @click.prevent="changePageByButton(true)">
                    <!-- Heroicon name: solid/arrow-narrow-left -->
                    <svg class="mr-3 h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                        <path fill-rule="evenodd" d="M7.707 14.707a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l2.293 2.293a1 1 0 010 1.414z" clip-rule="evenodd" />
                    </svg>
                    Previous
                </a>
            </div>
            <div class="hidden md:-mt-px md:flex">
                <a v-for="page in localModel.TotalPages"
                   :key="page"
                   href="#"
                   class="border-t-2 pt-4 px-4 inline-flex items-center text-sm font-medium"
                   :class="{'border-secondary text-hoverLight' : isPageSelected(page), 'border-transparent hover:text-hover hover:border-gray-300' : !isPageSelected(page)}"
                   aria-current="isPageSelected(page)"
                   @click.prevent="changePageByClick(page)">
                    {{page}}
                </a>
            </div>
            <div class="-mt-px w-0 flex-1 flex justify-end">
                <a href="#" class="border-t-2 border-transparent pt-3 pl-2 pr-1 inline-flex items-center text-sm font-medium hover:text-hover hover:border-gray-300" v-if="hasNext" @click.prevent="changePageByButton(false)">
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
    import vueTableColumn from '@/components/Tables/vueTableColumn';

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

            model: {
                type: Object,
                default: () => { }
            },

            columns: {
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

            searchFunction: {
                type: Function,
                required: true
            },

            hiddenColumns: {
                type: Array,
                default: () => []
            }
        },

        components: {
            'vue-select': fieldSelect,
            'vue-search-input': fieldSearchInput,
            'vue-table': vueTable,
            'vue-table-column': vueTableColumn,
        },

        mounted() {
            this.performSearch();
        },

        data() {
            return {
                localModel: this.cloneModel(this.convertToPagination(this.model)),
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
                searchValue: '',
                items: []
            }
        },

        methods: {
            perPageChange(page) {
                if (!this.showPerPage) {
                    return;
                };

                this.localModel.PerPage = page.value;

                this.performSearch();
            },

            searchFieldChange() {
                this.localModel.SearchTerm = this.searchValue;

                this.performSearch();
            },

            isPageSelected(page) {
                return this.localModel.CurrentPage === page;
            },

            editClick(e) {
                this.$emit('editClick', e)
            },

            changePageByButton(isSubtract = false) {
                debugger;
                if (!isSubtract) {
                    this.incrementPageNumber();
                    return;
                }

                this.decreasePageNumber();
            },

            changePageByClick(pageNumber) {
                this.localModel.CurrentPage = pageNumber;
                this.performSearch();
            },

            incrementPageNumber() {
                if (!this.hasNext) {
                    return;
                }

                this.localModel.CurrentPage += 1;
                this.performSearch();
            },

            decreasePageNumber() {
                if (!this.hasPrevious) {
                    return;
                }
                this.localModel.CurrentPage -= 1;
                this.performSearch();
            },

            async performSearch() {
                const tableRecords = this.cloneModel(await this.searchFunction(this.localModel));

                const totalRecords = tableRecords.TotalRecords
                delete tableRecords.TotalRecords

                let records = []

                Object.entries(tableRecords).forEach(entry => {
                    const [key, value] = entry;
                    records.push(value);
                });

                this.localModel.TotalPages = Math.ceil(totalRecords / this.localModel.PerPage);

                this.items = records;
            },

            setSort(sortProperties) {
                this.localModel.OrderBy = sortProperties.Prop;
                this.localModel.IsAscending = sortProperties.IsAscending;

                this.performSearch();
            }
        },

        computed: {
            hasPrevious() {
                return this.localModel.CurrentPage - 1 != 0;
            },
            hasNext() {
                return this.localModel.CurrentPage < this.localModel.TotalPages;
            }
        },

        watch: {
            searchValue(newVal, oldVal) {
                if (newVal !== oldVal) {
                    this.debounce(this.searchFieldChange, 2000);
                }
            },

            model(newVal, oldVal) {
                if (!this.areEquivalent(newVal, oldVal)) {
                    this.localModel = this.cloneModel(this.convertToPagination(newVal))
                }
            }
        }
    }
</script>