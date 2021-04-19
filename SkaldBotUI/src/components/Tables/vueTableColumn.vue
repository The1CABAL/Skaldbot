<template>
    <th scope="col" class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider" @click="handleSort">
        {{label}}
        <span v-if="isSortable" v-html="caretCode">
        </span>
    </th>
</template>

<script>
    export default {
        name: "TableColumn",

        props: {
            isSortable: {
                type: Boolean,
                default: false
            },
            label: {
                type: String,
                required: true
            }
        },

        data() {
            return {
                isAscending: false,
            }
        },

        methods: {
            handleSort() {
                if (!this.isSortable) {
                    return;
                }

                this.isAscending = !this.isAscending;

                this.$emit('sort', this.label);
            }
        },

        computed: {
            caretCode() {
                if (!this.isSortable) {
                    return;
                }

                if (this.isAscending) {
                    return '&#9650;'
                }

                return '&#9660;'
            }
        }
    }
</script>