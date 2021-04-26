<template>
    <div class="pt-2 pb-2 cursor-pointer">
        <label :for="name" class="flex justify-start items-start">
            <div class="bg-white rounded-md w-5 h-5 flex flex-shrink-0 justify-center items-center mr-2 focus-within:border-indigo-500">
                <input :id="id" :name="name" type="checkbox" class="opacity-0 absolute" @change="onChange" v-model="localValue">
                <svg v-show="localValue === true" class="fill-current w-4 h-4 text-secondary pointer-events-none" viewBox="0 0 20 20"><path d="M0 11l2-2 5 5L18 3l2 2L7 18z" /></svg>
            </div>
            <div class="select-none"><slot></slot></div>
        </label>
    </div>
</template>

<script>
    export default {
        name: "Checkbox",

        props: ['value', 'name', 'id'],

        data() {
            return {
                localValue: true
            }
        },

        mounted() {
            this.localValue = this.value || false;
        },

        methods: {
            onChange() {
                this.$emit('change');
                this.$emit('input', this.localValue);
            }
        },

        watch: {
            value(newVal, oldVal) {
                if (newVal !== oldVal) {
                    this.localValue = newVal;
                }
            }
        }
    }
</script>