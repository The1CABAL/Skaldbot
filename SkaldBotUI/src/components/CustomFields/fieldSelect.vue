<template>
    <div>
        <label id="listbox-label" class="block text-sm font-medium text-primary" v-if="label">
            {{label}}
        </label>
        <div class="mt-1 relative">
            <button @click="toggleList" type="button" class="relative w-full bg-white text-black border border-gray-300 rounded-md shadow-sm pl-3 pr-10 py-2 text-left cursor-default focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-secondary sm:text-sm" :aria-expanded="listToggled" aria-labelledby="listbox-label">
                <span class="block truncate">
                    {{selectedName}}
                </span>
                <span class="absolute inset-y-0 right-0 flex items-center pr-2 pointer-events-none">
                    <svg class="h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                        <path fill-rule="evenodd" d="M10 3a1 1 0 01.707.293l3 3a1 1 0 01-1.414 1.414L10 5.414 7.707 7.707a1 1 0 01-1.414-1.414l3-3A1 1 0 0110 3zm-3.707 9.293a1 1 0 011.414 0L10 14.586l2.293-2.293a1 1 0 011.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clip-rule="evenodd" />
                    </svg>
                </span>
            </button>

            <ul v-show="listToggled" class="absolute transition ease-in duration-100 mt-1 w-full bg-white shadow-lg max-h-60 rounded-md py-1 text-base ring-1 ring-black ring-opacity-5 overflow-auto focus:outline-none sm:text-sm" tabindex="-1" role="listbox" aria-labelledby="listbox-label" :id="selectListGeneratedId">
                <li class="cursor-default select-none relative py-2 pl-8 pr-4 hover:bg-hoverLight"
                    :class="{'text-primary' : !isSelectSelected, 'text-white bg-hover' : isSelectSelected}"
                    id="listbox-option-0"
                    role="option" @click="setItem('Select')" v-if="showSelectOption">
                    <span class="font-normal block truncate">
                        Select
                    </span>

                    <span class="text-secondary absolute inset-y-0 left-0 flex items-center pl-1.5" v-if="isSelectSelected">
                        <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                            <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                        </svg>
                    </span>
                </li>
                <li v-for="(option, index) in items" :key="option[valueKey]"
                    class="cursor-default select-none relative py-2 pl-8 pr-4 hover:bg-hoverLight"
                    :class="{'text-gray-900' : !showCheckmarkFor(option[nameKey]), 'text-white bg-indigo-400' : showCheckmarkFor(option[valueKey])}"
                    :id="getId(index)" role="option" @click="setItem(option)">
                    <span class="font-normal block truncate">
                        {{option[nameKey]}}
                    </span>
                    <span class="text-secondary absolute inset-y-0 left-0 flex items-center pl-1.5" v-if="showCheckmarkFor(option[valueKey])">
                        <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                            <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                        </svg>
                    </span>
                </li>
            </ul>
        </div>
    </div>
</template>

<script>
    export default {
        name: "Select",

        props: {
            label: {
                type: String,
                required: false
            },
            showSelectOption: {
                type: Boolean,
                required: false,
                default: true
            },
            nameKey: {
                type: String,
                default: 'name'
            },
            valueKey: {
                type: String,
                default: 'value'
            },
            items: {
                type: Array,
                default: () => []
            },
            defaultSelectedItem: {
                type: Number | String,
                required: false
            }
        },

        data() {
            return {
                selectedValue: '',
                selectedName: '',
                listToggled: false,
                selectListGeneratedId: '',
                selectedItem: {}
            }
        },

        beforeMount() {
            this.selectListGeneratedId = require('crypto').randomBytes(24)
                .toString('base64')
                .slice(0, 24)
        },

        methods: {
            setItem(item) {
                if (!item) {
                    return;
                }

                if (typeof item === 'object') {
                    this.selectedItem = item;
                    this.selectedValue = item[this.valueKey];
                    this.selectedName = item[this.nameKey];
                }
                else {
                    this.selectedItem = item;
                    this.selectedValue  = item;
                    this.selectedName  = item;
                }
                
                this.toggleList();

                if (this.selectedValue === "Select") {
                    
                    this.$emit('change', '');
                    return;
                }

                this.$emit('change', this.selectedItem);
            },

            showCheckmarkFor(currentItemKey) {
                if (typeof this.selectedItem !== 'object') {
                    return false;
                }
                return this.selectedItem[this.valueKey] === currentItemKey;
            },

            getId(index) {
                return `listbox-option-${index + 1}`
            },

            toggleList() {
                this.listToggled = !this.listToggled;
            },
        },

        computed: {
            isSelectSelected() {
                return this.selectedValue === 'Select';
            },
        },

        mounted() {
            if (!this.selectedValue) {
                if (this.showSelectOption) {
                    this.selectedName = 'Select'
                    this.selectedValue = 'Select'
                    this.selectedItem = 'Select'
                }
                else if (this.defaultSelectedItem) {
                    this.selectedItem = this.items.find(item => item[this.valueKey] === this.defaultSelectedItem);
                    this.selectedValue = this.selectedItem[this.valueKey];
                    this.selectedName = this.selectedItem[this.nameKey];
                }
            }
        }
    }
</script>

<style scoped>
</style>