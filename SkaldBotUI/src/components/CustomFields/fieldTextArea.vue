<template>
    <div class="pt-3 pb-3 sm:col-span-4 w-full">
        <label :for="name" class="block text-sm font-medium">
            <slot></slot>
        </label>
        <div class="mt-1 flex rounded-md shadow-sm">
            <textarea :id="id" :name="name"
                      class="block w-full cursor-pointer pl-3 pr-3 py-2 border border-transparent rounded-md leading-5  focus:outline-none focus:bg-gray-300 focus:text-primary focus:border-hover focus:ring-secondary sm:text-sm"
                      :class="{'cursor-not-allowed bg-gray-700 placeholder-gray-400 text-gray-400' : isDisabled, 'bg-gray-500' : !isDisabled}"
                      :disabled="isDisabled"
                      v-model="localValue"
                      :required="required"
                      :rows="rows">
            </textarea>
        </div>
    </div>
</template>

<script>
    export default {
        name: "fieldTextArea",

        props: ['value', 'id', 'name', 'isDisabled', 'required', 'rows'],

        data() {
            return {
                localValue: ''
            }
        },

        mounted() {
            this.localValue = this.value;
        },

        watch: {
            value(newVal, oldVal) {
                if (newVal !== oldVal && newVal !== this.localValue) {
                    this.localValue = newVal
                }
            },

            localValue(newVal, oldVal) {
                if (newVal !== oldVal) {
                    this.$emit('input', newVal);
                }
            }
        }
    }
</script>