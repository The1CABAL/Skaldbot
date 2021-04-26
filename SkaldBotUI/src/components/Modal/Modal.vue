<template>
    <transition name="modal-fade">
        <div class="fixed z-10 inset-0 overflow-y-auto text-white" aria-labelledby="modal-title" role="dialog" aria-modal="true">
            <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
                <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" aria-hidden="true"></div>
                <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
                <div class="inline-block align-bottom bg-primary rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-3xl sm:w-full sm:p-6">
                    <div class="text-right">
                        <p class="cursor-pointer" @click="close">
                            &#10006;
                        </p>
                    </div>
                    <div class="w-full">
                        <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full" v-if="hasSvg">
                            <slot name="svg"></slot>
                        </div>
                        <div class="mt-3 sm:mt-5">
                            <h3 class="text-lg leading-6 font-medium" id="modal-title">
                                <slot name="title">

                                </slot>
                            </h3>
                            <div class="mt-2">
                                <p class="text-sm">
                                    <slot name="body">

                                    </slot>
                                </p>
                            </div>
                        </div>
                    </div>
                    <div class="flex flex-1 justify-center space-x-2 mt-2" v-if="hasActionButtons">
                        <slot name="actionButtons">
                        </slot>
                    </div>
                </div>
            </div>
        </div>
    </transition>
</template>

<script>
    export default {
        name: "Modal",

        computed: {
            hasSvg() {
                return this.$slots.svg !== undefined && this.$slots.svg.length > 0;
            },

            hasActionButtons() {
                return this.$slots.actionButtons.length > 0;
            }
        },

        methods: {
            close() {
                this.$emit('close')
            }
        }
    }
</script>